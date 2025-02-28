import { app, BrowserWindow } from "electron";
import * as path from "path";
import * as url from "url";

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 700,
    backgroundColor: "#f2f2f2",
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      devTools: process.env.NODE_ENV !== "production",
    },
  });

  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:4000");
  } else {
    mainWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, "renderer/index.html"),
        protocol: "file:",
        slashes: true,
      })
    );
  }

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

// Some APIs can only be used after this event occurs.
app.on("ready", createWindow);

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
