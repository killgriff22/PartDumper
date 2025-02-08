infile = open("in.txt", "r")
badchars = [
    " ",
    "-",
    "",
    ",",
    ":",
    ";",
    "'",
    "\"",
    "/",
    "\\",
    "|",
    "[",
    "]",
    "{",
    "}",
    "(",
    ")",
    "<",
    ">",
    "?",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "+",
    "=",
    "~",
    "`"
]
def single(data):
    outfile = open("Partlib.lua", "a")
    data = data.split("\n")
    data = [[0,x.split("[Message:     Unity] Lua: ")[-1]][1] for x in data]
    empty = []
    for i, x in enumerate(data):
        print(f"{i}: {x}")
        if not x:
            empty.append(i)
    for i,x in enumerate(empty):
        data.pop(x+i)
    in_data_values = [x.split(":")[1].strip() for x in data]
    in_data_names = [x.split(":")[0] for x in data]
    for i, x in enumerate(in_data_values):
        for b, char in enumerate(x):
            if char in badchars:
                in_data_values[i] = in_data_values[i].replace(char, "_")
    partdesc = {
        "AssetName": in_data_values[1],
        "Category": in_data_values[2],
        "DisplayName": in_data_values[4],
        "IsResizable": in_data_values[6],
        "IsPaintable": in_data_values[7],
        "IsMaterialSwappable": in_data_values[8],
        "UnitVolume": in_data_values[11],
        "Mass": in_data_values[12],
        "Strength": in_data_values[13],
        "Properties" : {
                "Material": in_data_values[15],
                "Density": in_data_values[16],
                "Mass": in_data_values[17],
                "Strength": in_data_values[18]
            },
        "Behaviors": {} if len(in_data_values)> 19 else "nil"
    }
    if len(in_data_values) > 19:
        currentbehaviour = ""
        for i, x in enumerate(in_data_values[19:]):
            if in_data_names[i + 19].strip() == "Behavior":
                currentbehaviour = x
                partdesc["Behaviors"][x] = {
                    "IsTweakable": in_data_values[i + 20],
                    "Channels": []
                }
            elif in_data_names[i + 19].strip() == "Channel":
                if currentbehaviour == "":
                    print("Error: Channel without behaviour")
                    exit()
                partdesc["Behaviors"][currentbehaviour]["Channels"].append(x)
    print("--")
    for key in partdesc:
        if key == "Behaviors" and not partdesc[key] == "nil":
            print(f"Behaviors: ")
            for behaviour in partdesc[key]:
                print(f"\tBehaviour: {behaviour}")
                for behaviourkey in partdesc[key][behaviour]:
                    print(f"\t\t{behaviourkey}: {partdesc[key][behaviour][behaviourkey]}")
        elif key == "Properties":
            print(f"Properties: ")
            for property in partdesc[key]:
                print(f"\t{property}: {partdesc[key][property]}")
        else:
            print(f"{key}: {partdesc[key]}")
    print("--")
    template = f"""
        {partdesc["AssetName"].replace(" ","_")} = {"{"}
            AssetName = "{partdesc["AssetName"]}",
            DisplayName = "{partdesc["DisplayName"]}",
            Category = "{partdesc["Category"]}",
            IsResizable = {partdesc['IsResizable']},
            IsPaintable = {partdesc['IsPaintable']},
            IsMaterialSwappable = {partdesc["IsMaterialSwappable"]},
            UnitVolume = {partdesc["UnitVolume"]},
            Mass = {partdesc["Mass"]},
            Strength = {partdesc["Strength"]},
            Properties = {"{"}
                Material = "{partdesc["Properties"]["Material"]}",
                Density = {partdesc["Properties"]["Density"]},
                Mass = {partdesc["Properties"]["Mass"]},
                Strength = {partdesc["Properties"]["Strength"]}
            {"}"},
            Behaviors = {"{" if partdesc["Behaviors"] != "nil" else "nil"}"""
    if partdesc["Behaviors"] != "nil":
        for behaviour in partdesc["Behaviors"]:
            template += f"""
                {behaviour.replace(" ","_")} = {"{"}
                    IsTweakable = {partdesc["Behaviors"][behaviour]["IsTweakable"]},
                    Channels = {"{"}"""
            for channel in partdesc["Behaviors"][behaviour]["Channels"]:
                template += f"""
                        \"{channel.strip()}\","""
            template += f"""
                    {"}"},
                {"}"},
    """
    template += f"""        {"}" if partdesc["Behaviors"] != "nil" else ""}
        {"}"},"""
    outfile.write(template)
    print(template)
    outfile.close()