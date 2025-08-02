local window = nil
local dumpbutton = nil
local Player =  LocalPlayer.value
local buttonwidth = 120
local buttonheight = 30
local partlabel = nil
local localPlayer = LocalPlayer.Value
local keypressed = false
local function GetTargetedPart()
    local targetedPart
    if localPlayer and localPlayer.Targeter then
        targetedPart = localPlayer.Targeter.TargetedPart
    else
        return nil
    end
    return targetedPart
end
local function catbool(text, bool)
    if bool then
        return text .. 'true'
    else
        return text .. 'false'
    end
end
local function dumpPart(part)
    local intrest_behavior = nil
    local part = GetTargetedPart() or part
    if not part then
        return
    end
    print("--..--..--")
    print('    AssetName: ' .. part.AssetName)
    print('    Category: ' .. part.Category)
    print('    AssetGUID: ' .. part.AssetGUID)
    print('    DisplayName: ' .. part.DisplayName)
    print('    FullDisplayName: ' .. part.FullDisplayName)
    print(catbool('    IsResizable: ', part.IsResizable))
    print(catbool('    IsPaintable: ', part.IsPaintable))
    print(catbool('    IsMaterialSwappable: ', part.IsMaterialSwappable))
    print(catbool('    IsVisible: ', part.IsVisible))
    print(catbool('    IsCollidable: ', part.IsCollidable))
    print('    UnitVolume: ' .. part.UnitVolume)
    print('    Mass: ' .. part.Mass)
    print('    Strength: ' .. part.Strength)
    print('    Properties:')
    print('        MaterialName: ' .. part.Properties.MaterialName)
    print('        Density: ' .. part.Properties.Density)
    print('        Mass: ' .. part.Properties.Mass)
    print('        Strength: ' .. part.Properties.Strength)
    print("    Behaviors:")
    for behavior in part.Behaviours do
        intrest_behavior = behavior
        print("    Behavior: " .. behavior.Name)
        print(catbool("        IsTweakable:", behavior.IsTweakable))
        for channel in behavior.Channels do
            print("        Channel: " .. channel.Label)
        end
    end
    print("--..--..--!")
end

local function CreateWindow(l, w, closefunc)
    local localwindow
    localwindow = Windows.CreateWindow()
    localwindow.SetAlignment(align_RightEdge, 20, l)
    localwindow.SetAlignment(align_TopEdge, 80, w)
    localwindow.OnClose.add(closefunc)
    localwindow.Title = ""
    localwindow.Show(true)
    return localwindow
end
local function CreateLabel(x,y,w,h,txt,localwindow)
    local lbl = localwindow.CreateLabel()
    lbl.SetAlignment(align_RightEdge,  x, w)
    lbl.SetAlignment(align_TopEdge,  y, h)
    lbl.Text = txt
    return lbl
    
end
local function CreateButton(x,y,w,h,txt,localwindow,clickfunc)
    local btn = localwindow.CreateTextButton()
    btn.SetAlignment(align_RightEdge,  x, w)
    btn.SetAlignment(align_TopEdge,  y, h)
    btn.OnClick.add( clickfunc )
    btn.Text = txt
end
local function createSlider(x,y,w,h,localwindow, min, max, default)
    local slider = localwindow.CreateSlider()
    slider.SetAlignment( align_RightEdge, x, w )
    slider.SetAlignment( align_TopEdge, y, h )
    slider.MinValue = min
    slider.MaxValue = max
    slider.Value = default
    return slider
end
local function onWindowClose()
    UnloadScript.Raise(ScriptName) -- Window closed, so unload this script.
end

local function populatemainwin()

    window = CreateWindow(buttonwidth, buttonheight*2, onWindowClose)
    window.Title = 'Part Dumper'
    dumpbutton = CreateButton(0, buttonheight, buttonwidth, buttonheight, 'Dump Part (tab)', window, dumpPart)
    partlabel = CreateLabel(0, 0, buttonwidth, buttonheight, 'Part: None', window)
end

populatemainwin()
function Update()
    local part = GetTargetedPart()
    if not part then
        partlabel.Text = 'Part: None'
    else
        partlabel.Text = 'Part: ' .. part.AssetName    
    end
    if Input.GetKey('tab') and not keypressed then
        keypressed = true
        for _part in Parts.Instances do
            dumpPart(_part)
        end
    elseif not Input.GetKey('tab') then
        keypressed= false
    end
end
function Cleanup()
    Windows.DestroyWindow(window)
end

