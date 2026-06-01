from pyscript import document

print("test.py loaded!")

def hello(event):
    name = document.getElementById("name_box").value

    document.getElementById(
        "output"
    ).innerText = f"Hello {name}"