; Set the base directory where the folder will be created
baseDirectory := "C:\\Users\\ReynoldsPurge\\Toyota of Hackensack\\TOH - Deals"

; Define the source and destination directories for file moving
sourceDirectory := baseDirectory . "\\2023 Scans"
destinationDirectory := baseDirectory . "\\Import"

; Initialize a variable to track if any files have been moved
filesMoved := false

; Move files from the source directory to the destination directory
Loop, Files, % sourceDirectory . "\\*.*", F
{
    fileName := A_LoopFileName
    ; Check if the file name has at least 6 digits
    numDigits := 0
    Loop, Parse, fileName
    {
        if (A_LoopField >= "0" && A_LoopField <= "9")
            numDigits++
    }

    if (numDigits >= 6)
    {
        FileMove, % A_LoopFileFullPath, % destinationDirectory . "\\"
        filesMoved := true
    }
}

; Only create the current date directory if files have been moved
if (filesMoved)
{
    ; Get the current date in YYYY-MM-DD format
    FormatTime, CurrentDate,, yyyy-MM-dd

    ; Combine the base directory with the current date to form the new directory path
    dateDirectory := baseDirectory . "\\" . CurrentDate

    ; Create the new directory if it doesn't exist
    if !FileExist(dateDirectory)
        FileCreateDir, %dateDirectory%
}

; Set the directory you want to list files from (now the 'Import' directory)
directoryPath := destinationDirectory

; Set the path and name of the CSV file to create back to its original location
csvFilePath := "R:\\filelist.csv"

; Set the path and name of the text file to create if no files are found back to its original location
noImportFilePath := "R:\\noimport.txt"

; Check if directory exists
if !FileExist(directoryPath . "\\")
{
    return
}

; Check if the directory is empty
FileCount := 0
Loop, Files, % directoryPath . "\\*.*", F
    FileCount++

; If the directory is empty, create noimport.txt and exit
if FileCount = 0
{
    File := FileOpen(noImportFilePath, "w") ; Open the file for writing
    File.Close()  ; Close the file
    return
}

; Otherwise, proceed to create the CSV file
FileDelete, %csvFilePath%  ; Delete the file if it exists
File := FileOpen(csvFilePath, "w") ; Open the file for writing
File.Encoding := "UTF-8"  ; Set file encoding to UTF-8

Loop, Files, % directoryPath . "\\*.*", F
{
    fullPath := A_LoopFileFullPath
    formattedPath := StrReplace(fullPath, "\\", "\") ; Replace \\ with \
    fileName := GetFileNameNoExt(formattedPath)
    File.Write(formattedPath . "," . fileName . "`r`n")  ; Comma-separated values
}

File.Close()  ; Close the file

; Function to get file name without extension and duplicate number
GetFileNameNoExt(fullPath) {
    SplitPath, fullPath, name, dir, ext, name_no_ext, drive
    ; Remove duplicate number indicator like (1), (2), etc.
    name_no_ext := RegExReplace(name_no_ext, " \(\d+\)$")
    return name_no_ext
}
