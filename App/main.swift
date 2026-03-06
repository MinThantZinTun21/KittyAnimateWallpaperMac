import Cocoa
import WebKit

class AppDelegate: NSObject, NSApplicationDelegate {
    
    private var window: NSWindow!
    private var webView: WKWebView!
    private var statusItem: NSStatusItem!
    private var cursorMonitor: Any?
    private var lastWallpaper: String = ""
    private var patternsPath: URL!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        findPatternsFolder()
        setupWindow()
        setupStatusBar()
        setupCursorTracking()
        
        if !lastWallpaper.isEmpty {
            loadWallpaper(lastWallpaper)
        }
    }
    
    func applicationWillTerminate(_ notification: Notification) {
        if let monitor = cursorMonitor {
            NSEvent.removeMonitor(monitor)
        }
    }
    
    private func findPatternsFolder() {
        guard let resourcePath = Bundle.main.resourcePath else {
            print("Error: No resource path found")
            return
        }
        
        let testPath = URL(fileURLWithPath: resourcePath)
        print("Resource path: \(testPath)")
        
        patternsPath = testPath.appendingPathComponent("Wallpapers/patterns")
        print("Patterns path: \(patternsPath)")
        
        if FileManager.default.fileExists(atPath: patternsPath.path) {
            print("Patterns folder exists")
        } else {
            print("Patterns folder NOT found, trying root Resources path")
            patternsPath = testPath
            print("Using root Resources path: \(patternsPath)")
        }
        
        loadFirstPattern()
    }
    
    private func loadFirstPattern() {
        do {
            let files = try FileManager.default.contentsOfDirectory(at: patternsPath, includingPropertiesForKeys: nil)
            let htmlFiles = files.filter { $0.pathExtension == "html" && $0.lastPathComponent != "index.html" }
            
            if let first = htmlFiles.sorted(by: { $0.lastPathComponent < $1.lastPathComponent }).first {
                lastWallpaper = first.lastPathComponent
            }
        } catch {
            print("Error: \(error)")
        }
    }
    
    private func setupWindow() {
        guard let screen = NSScreen.main else { return }
        
        window = NSWindow(
            contentRect: screen.frame,
            styleMask: .borderless,
            backing: .buffered,
            defer: false
        )
        
        window.isOpaque = true
        window.backgroundColor = NSColor(red: 0.1, green: 0.1, blue: 0.15, alpha: 1.0)
        window.hasShadow = false
        window.level = .init(rawValue: Int(CGWindowLevelForKey(.desktopWindow)))
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .ignoresCycle]
        window.isReleasedWhenClosed = false
        window.ignoresMouseEvents = true
        
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
        
        webView = WKWebView(frame: screen.frame, configuration: config)
        webView.setValue(false, forKey: "drawsBackground")
        
        window.contentView = webView
        window.orderFront(nil)
    }
    
    private func setupStatusBar() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "paintpalette", accessibilityDescription: "Wallpaper")
            button.imagePosition = .imageOnly
        }
        
        let menu = NSMenu()
        
        guard patternsPath != nil else {
            print("Error: patternsPath is nil")
            addErrorItems(to: menu)
            statusItem.menu = menu
            return
        }
        
        guard let files = try? FileManager.default.contentsOfDirectory(at: patternsPath, includingPropertiesForKeys: nil) else {
            print("Error: Cannot read patterns directory: \(patternsPath)")
            addErrorItems(to: menu)
            statusItem.menu = menu
            return
        }
        
        let htmlFiles = files
            .filter { $0.pathExtension == "html" && $0.lastPathComponent != "index.html" }
            .sorted { $0.lastPathComponent < $1.lastPathComponent }
        
        if htmlFiles.isEmpty {
            print("Error: No HTML files found in: \(patternsPath)")
            addErrorItems(to: menu)
            statusItem.menu = menu
            return
        }
        
        print("Found \(htmlFiles.count) wallpaper files")
        
        for fileURL in htmlFiles {
            let filename = fileURL.lastPathComponent
            let name = filename.replacingOccurrences(of: ".html", with: "")
                .replacingOccurrences(of: "-", with: " ")
                .split(separator: " ")
                .map { $0.prefix(1).uppercased() + $0.dropFirst().lowercased() }
                .joined(separator: " ")
            
            let item = NSMenuItem(title: name, action: #selector(wallpaperChosen(_:)), keyEquivalent: "")
            item.target = self
            item.representedObject = filename
            menu.addItem(item)
        }
        
        menu.addItem(NSMenuItem.separator())
        
        let reloadItem = NSMenuItem(title: "Reload", action: #selector(reloadWallpaper), keyEquivalent: "r")
        reloadItem.target = self
        menu.addItem(reloadItem)
        
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    private func addErrorItems(to menu: NSMenu) {
        let errorItem = NSMenuItem(title: "Error loading wallpapers", action: nil, keyEquivalent: "")
        errorItem.isEnabled = false
        menu.addItem(errorItem)
        
        menu.addItem(NSMenuItem.separator())
        
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
    }
    
    @objc private func wallpaperChosen(_ sender: NSMenuItem) {
        if let file = sender.representedObject as? String {
            lastWallpaper = file
            loadWallpaper(file)
        }
    }
    
    @objc private func reloadWallpaper() {
        loadWallpaper(lastWallpaper)
    }
    
    @objc private func quitApp() {
        NSApplication.shared.terminate(nil)
    }
    
    private func loadWallpaper(_ filename: String) {
        let fileURL = patternsPath.appendingPathComponent(filename)
        webView.loadFileURL(fileURL, allowingReadAccessTo: patternsPath)
    }
    
    private func setupCursorTracking() {
        cursorMonitor = NSEvent.addGlobalMonitorForEvents(matching: [.mouseMoved, .leftMouseDragged]) { [weak self] event in
            self?.sendCursorPosition(event.locationInWindow)
        }
    }
    
    private func sendCursorPosition(_ location: NSPoint) {
        guard let screen = NSScreen.main else { return }
        
        let normalizedX = location.x / screen.frame.width
        let normalizedY = 1.0 - (location.y / screen.frame.height)
        
        let js = """
        (function() {
            var event = new CustomEvent('cursorMove', {
                detail: { x: \(normalizedX), y: \(normalizedY), screenX: \(location.x), screenY: \(location.y) }
            });
            window.dispatchEvent(event);
        })();
        """
        
        webView.evaluateJavaScript(js, completionHandler: nil)
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
