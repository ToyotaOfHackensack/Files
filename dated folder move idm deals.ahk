; Set the source directory where the date-named folder is located
sourceDirectory := "C:\\Users\\ReynoldsPurge\\Toyota of Hackensack\\TOH - Deals"

; Set the destination directory where the new date-named folder will be created
destinationDirectory := "C:\\Users\\ReynoldsPurge\\Toyota of Hackensack\\TOH - Imported to IDM"

; Define the path for the log file
logFilePath := "C:\\Users\\ReynoldsPurge\\Toyota of Hackensack\\FolderMoveLog.txt"

; Get the current date in YYYY-MM-DD format
FormatTime, CurrentDate,, yyyy-MM-dd

; Combine the source directory with the current date to form the folder path
dateFolderPath := sourceDirectory . "\\" . CurrentDate

; Define the destination path for the new date-named folder
destinationFolderPath := destinationDirectory . "\\" . CurrentDate

; Open the log file for writing
LogFile := FileOpen(logFilePath, "a")
LogFile.Encoding := "UTF-8"

; Check if the source date-named folder exists
if FileExist(dateFolderPath)
{
    ; Create the new folder at the destination
    FileCreateDir, %destinationFolderPath%

    ; Try to move all contents from the source folder to the new folder
    try
    {
        Loop, Files, %dateFolderPath%\*.*, F
            FileMove, %A_LoopFileFullPath%, %destinationFolderPath%\
        
        Loop, Files, %dateFolderPath%\*.*, D
            FileMoveDir, %A_LoopFileFullPath%, %destinationFolderPath%\

        LogFile.WriteLine(A_Now . " - Moved all contents from: " . dateFolderPath . " to " . destinationFolderPath)

        ; Delete the old folder after moving its contents
        FileRemoveDir, %dateFolderPath%, 1
        LogFile.WriteLine(A_Now . " - Deleted old folder: " . dateFolderPath)
    }
    catch e
    {
        LogFile.WriteLine(A_Now . " - Error moving contents or deleting old folder: " . e.message)
    }
}
else
{
    LogFile.WriteLine(A_Now . " - Source folder does not exist: " . dateFolderPath)
}

; Close the log file
LogFile.Close()
