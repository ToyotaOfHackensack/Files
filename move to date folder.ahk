; Set the base directory where the date-named folder is located
baseDirectory := "C:\\Users\\ReynoldsPurge\\Toyota of Hackensack\\TOH - Deals"

; Get the current date in YYYY-MM-DD format
FormatTime, CurrentDate,, yyyy-MM-dd

; Combine the base directory with the current date to form the new directory path
dateDirectory := baseDirectory . "\\" . CurrentDate

; Create the new directory if it doesn't exist
if !FileExist(dateDirectory)
    FileCreateDir, %dateDirectory%

; Get the file path from the clipboard
filePath := Clipboard

; Check if the clipboard content is a valid file path
if !FileExist(filePath)
{
    MsgBox, The clipboard does not contain a valid file path.
    return
}

; Extract filename from the file path
SplitPath, filePath, fileName

; Define the destination path
destinationPath := dateDirectory . "\\" . fileName

; Move the file to the destination
FileMove, %filePath%, %destinationPath%