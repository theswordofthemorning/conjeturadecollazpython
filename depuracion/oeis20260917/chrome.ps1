param(
    [ValidateSet('leer', 'ir', 'arbol', 'captura', 'teclas', 'clic', 'pegar', 'copiar')]
    [string]$Accion = 'leer',
    [string]$Valor = ''
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class RatonOeis {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint x, uint y, uint data, UIntPtr extra);
    public static void Clic(int x, int y) {
        SetCursorPos(x, y);
        mouse_event(2, 0, 0, 0, UIntPtr.Zero);
        mouse_event(4, 0, 0, 0, UIntPtr.Zero);
    }
}
'@
$control = New-Object -ComObject WScript.Shell
$condicion = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::ClassNameProperty,
    'Chrome_WidgetWin_1')
$ventana = [System.Windows.Automation.AutomationElement]::RootElement.FindFirst(
    [System.Windows.Automation.TreeScope]::Children, $condicion)
if ($null -eq $ventana) { throw 'No se encontro Chrome' }
if (-not $control.AppActivate($ventana.Current.ProcessId)) { throw 'No se activo Chrome' }
Start-Sleep -Milliseconds 300

switch ($Accion) {
    'copiar' {
        [System.Windows.Forms.SendKeys]::SendWait('^a')
        [System.Windows.Forms.SendKeys]::SendWait('^c')
        Start-Sleep -Milliseconds 300
        $contenido = [System.Windows.Forms.Clipboard]::GetText()
        if ($Valor -notmatch '^[A-Za-z0-9_-]+\.txt$') { throw 'Nombre local invalido' }
        [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $Valor), $contenido)
        [Console]::WriteLine($contenido)
    }
    'clic' {
        $coordenadas = $Valor.Split(',')
        [RatonOeis]::Clic([int]$coordenadas[0], [int]$coordenadas[1])
        Start-Sleep -Milliseconds 500
    }
    'pegar' {
        $contenido = Get-Content -LiteralPath $Valor -Encoding UTF8 -Raw
        [System.Windows.Forms.Clipboard]::SetText($contenido)
        [System.Windows.Forms.SendKeys]::SendWait('^v')
        Start-Sleep -Milliseconds 300
    }
    'ir' {
        if ($Valor -notmatch '^https://oeis\.org/') { throw 'Solo se permite navegar a OEIS' }
        [System.Windows.Forms.Clipboard]::SetText($Valor)
        [System.Windows.Forms.SendKeys]::SendWait('^l')
        [System.Windows.Forms.SendKeys]::SendWait('^v')
        [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
        Start-Sleep -Seconds 3
    }
    'teclas' {
        [System.Windows.Forms.SendKeys]::SendWait($Valor)
        Start-Sleep -Milliseconds 500
    }
    'leer' {
        [System.Windows.Forms.SendKeys]::SendWait('{ESC}')
        [RatonOeis]::Clic(350, 350)
        [System.Windows.Forms.SendKeys]::SendWait('^a')
        [System.Windows.Forms.SendKeys]::SendWait('^c')
        Start-Sleep -Milliseconds 300
        $contenido = [System.Windows.Forms.Clipboard]::GetText()
        if ($Valor -match '^[A-Za-z0-9_-]+\.txt$') {
            [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $Valor), $contenido)
        }
        [Console]::WriteLine($contenido)
    }
    'arbol' {
        $elementos = $ventana.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach ($elemento in $elementos) {
            $c = $elemento.Current
            if ($c.Name) {
                [Console]::WriteLine('{0} | {1} | {2}',
                    $c.ControlType.ProgrammaticName, $c.AutomationId, $c.Name)
            }
        }
    }
    'captura' {
        $rectangulo = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $mapa = New-Object System.Drawing.Bitmap($rectangulo.Width, $rectangulo.Height)
        $grafico = [System.Drawing.Graphics]::FromImage($mapa)
        $grafico.CopyFromScreen($rectangulo.Location, [System.Drawing.Point]::Empty, $rectangulo.Size)
        $destino = Join-Path $PSScriptRoot 'chrome.png'
        $mapa.Save($destino)
        $grafico.Dispose()
        $mapa.Dispose()
        [Console]::WriteLine($destino)
    }
}
