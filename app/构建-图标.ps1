# 生成应用图标（icon-192 / icon-512 / apple-touch-icon），印章风格：朱砂底 + 白色"诗"字
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path

function New-AppIcon([int]$size, [string]$file) {
    $bmp = New-Object System.Drawing.Bitmap($size, $size)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

    # 朱砂底（全出血，兼容 maskable）
    $bg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(179, 70, 57))
    $g.FillRectangle($bg, 0, 0, $size, $size)

    # 内框（印章边线）
    $inset = [single]($size * 0.10)
    $r = [single]($size * 0.07)
    $d = 2 * $r
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddArc($inset, $inset, $d, $d, 180, 90)
    $path.AddArc($size - $inset - $d, $inset, $d, $d, 270, 90)
    $path.AddArc($size - $inset - $d, $size - $inset - $d, $d, $d, 0, 90)
    $path.AddArc($inset, $size - $inset - $d, $d, $d, 90, 90)
    $path.CloseAllFigures()
    $penW = [single]($size * 0.022)
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 246, 234), $penW)
    $g.DrawPath($pen, $path)

    # 白色"诗"字（宋体）
    $fontPx = [int]($size * 0.50)
    $font = New-Object System.Drawing.Font("SimSun", $fontPx, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF(0, 0, $size, $size)
    $g.DrawString("诗", $font, [System.Drawing.Brushes]::White, $rect, $sf)

    $out = Join-Path $dir $file
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Host "已生成 $file（$size x $size）"
}

New-AppIcon 192 "icon-192.png"
New-AppIcon 512 "icon-512.png"
New-AppIcon 180 "apple-touch-icon.png"
