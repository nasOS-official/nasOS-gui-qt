import os
for file in os.listdir("/usr/share/applications/"):
    if file.endswith(".desktop"):
        filer = open(os.path.join("/usr/share/applications/", file), "r")
        for line in filer:
            if line.find('[') == 0:
                current_section = line.rstrip("\n")
            if current_section == """[Desktop Entry]""":
                splited_line = line.rstrip("\n").split("=")
                if splited_line[0] == "Name":
                    name = splited_line[1]
                elif splited_line[0] == "Exec":
                    execute = splited_line[1]
                elif splited_line[0] == "Icon":
                    icon = splited_line[1]
        print(f"""===========
Имя: {name}
Команда запуска: {execute}
Иконка {icon}""")

