"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const askPythonPath = vscode.workspace.getConfiguration('napkin').get('askPythonPath');
const trainPythonPath = vscode.workspace.getConfiguration('napkin').get('trainPythonPath');
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "Napkin" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let helpCmd = vscode.commands.registerCommand('napkin.help', () => {
        vscode.window.showInformationMessage('This is a help message');
    });
    let askCmd = vscode.commands.registerCommand('napkin.ask', () => {
        // Get user input for arguments to pass to python
        let inputBoxOptions = {
            prompt: "Enter your question",
            placeHolder: "args"
        };
        vscode.window.showInputBox(inputBoxOptions).then((value) => {
            if (value === undefined) {
                return;
            }
            let args = value;
            let command = 'python3 ' + askPythonPath + ' ' + args;
            (0, child_process_1.exec)(command, (error, stdout, stderr) => {
                if (error) {
                    console.log(`error: ${error.message}`);
                }
                else if (stderr) {
                    console.log(`stderr: ${stderr}`);
                }
                else {
                    console.log(stdout);
                }
            });
        });
    });
    let trainCmd = vscode.commands.registerCommand('napkin.train', () => {
        // Get user input for arguments to pass to python
        let inputBoxOptions = {
            prompt: "Enter Training Arguments",
            placeHolder: "args"
        };
        vscode.window.showInputBox(inputBoxOptions).then((value) => {
            if (value === undefined) {
                return;
            }
            let args = value;
            let command = 'python3 ' + trainPythonPath + ' ' + args;
            (0, child_process_1.exec)(command, (error, stdout, stderr) => {
                if (error) {
                    console.log(`error: ${error.message}`);
                }
                else if (stderr) {
                    console.log(`stderr: ${stderr}`);
                }
                else {
                    console.log(stdout);
                }
            });
        });
    });
    context.subscriptions.push(helpCmd, askCmd, trainCmd);
}
exports.activate = activate;
// This method is called when your extension is deactivated
function deactivate() {
    console.log("Napkin Deactivated");
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map