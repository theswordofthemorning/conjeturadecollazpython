param(
    [ValidateSet('leer', 'enlace', 'controles', 'buscar', 'valor', 'obtener', 'boton')]
    [string]$Accion = 'leer',
    [string]$Valor = '',
    [string]$Archivo = '',
    [int]$Indice = 0,
    [switch]$Silencio
)

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$raiz = [System.Windows.Automation.AutomationElement]::RootElement
$condicion = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::ClassNameProperty, 'Chrome_WidgetWin_1')
$ventanas = $raiz.FindAll([System.Windows.Automation.TreeScope]::Children, $condicion)
$ventana = @($ventanas | Where-Object { $_.Current.Name -match 'OEIS|Integer Sequences' })[0]
if ($null -eq $ventana) { throw 'No se encontro la ventana OEIS' }
$condicionDocumento = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
    [System.Windows.Automation.ControlType]::Document)
$documento = $ventana.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condicionDocumento)
if ($null -eq $documento) { throw 'No se encontro documento OEIS' }
$elementos = $documento.FindAll([System.Windows.Automation.TreeScope]::Descendants,
    [System.Windows.Automation.Condition]::TrueCondition)

switch ($Accion) {
    'leer' {
        $patron = $null
        if ($documento.TryGetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern, [ref]$patron)) {
            $texto = $patron.DocumentRange.GetText(-1)
        } else {
            $texto = ($elementos | ForEach-Object { $_.Current.Name }) -join "`n"
        }
        if ($Archivo) { [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $Archivo), $texto) }
        if (-not $Silencio) { [Console]::WriteLine($texto) }
    }
    'controles' {
        foreach ($elemento in $elementos) {
            $c = $elemento.Current
            if ($c.ControlType -in @([System.Windows.Automation.ControlType]::Edit,
                    [System.Windows.Automation.ControlType]::Button)) {
                $patron = $null
                $contenido = ''
                if ($elemento.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$patron)) {
                    $contenido = $patron.Current.Value
                }
                [Console]::WriteLine('{0} | {1} | {2} | {3} | {4}',
                    $c.ControlType.ProgrammaticName, $c.AutomationId, $c.Name, $c.BoundingRectangle, $contenido)
            }
        }
    }
    'enlace' {
        $coinciden = @($elementos | Where-Object {
            $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Hyperlink -and $_.Current.Name -eq $Valor
        })
        if ($coinciden.Count -le $Indice) { throw 'Enlace no encontrado' }
        ([System.Windows.Automation.InvokePattern]$coinciden[$Indice].GetCurrentPattern(
            [System.Windows.Automation.InvokePattern]::Pattern)).Invoke()
    }
    'buscar' {
        $campo = @($elementos | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and $_.Current.Name -eq 'Search Query' })[0]
        ([System.Windows.Automation.ValuePattern]$campo.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)).SetValue($Valor)
        $boton = @($elementos | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and $_.Current.Name -eq 'Search' })[0]
        ([System.Windows.Automation.InvokePattern]$boton.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)).Invoke()
    }
    'valor' {
        $campos = @($elementos | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit })
        if ($Archivo) { $Valor = Get-Content -LiteralPath (Join-Path $PSScriptRoot $Archivo) -Encoding utf8 -Raw }
        ([System.Windows.Automation.ValuePattern]$campos[$Indice].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)).SetValue($Valor)
        Start-Sleep -Milliseconds 500
        $campos[$Indice].SetFocus()
    }
    'obtener' {
        $campos = @($elementos | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit })
        $campos[$Indice].SetFocus()
        Start-Sleep -Milliseconds 500
        $texto = ([System.Windows.Automation.ValuePattern]$campos[$Indice].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)).Current.Value
        if ($Archivo) { [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $Archivo), $texto) }
        if (-not $Silencio) { [Console]::WriteLine($texto) }
    }
    'boton' {
        $botones = @($elementos | Where-Object { $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and $_.Current.Name -eq $Valor })
        if ($botones.Count -le $Indice) { throw 'Boton no encontrado' }
        ([System.Windows.Automation.InvokePattern]$botones[$Indice].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)).Invoke()
    }
}
if ($Accion -in @('enlace', 'buscar', 'boton', 'valor')) { Start-Sleep -Seconds 2 }
