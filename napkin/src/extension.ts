// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { exec } from 'child_process';

const askPythonPath = vscode.workspace.getConfiguration('napkin').get('askPythonPath');
const trainPythonPath = vscode.workspace.getConfiguration('napkin').get('trainPythonPath');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

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
			exec(command, (error, stdout, stderr) => {
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
			exec(command, (error, stdout, stderr) => {
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

// This method is called when your extension is deactivated
export function deactivate() {
	console.log("Napkin Deactivated");
}