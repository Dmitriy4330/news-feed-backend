# Скрипт для конвертации всех Python файлов в UTF-8
$files = Get-ChildItem -Recurse -Filter *.py

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    # Сохраняем в UTF-8 без BOM
    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
    Write-Host "✅ Конвертирован: $($file.FullName)"
}

Write-Host "`nГотово! Все файлы конвертированы в UTF-8"