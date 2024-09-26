import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID")  # ID de la página donde crearás la nueva subpágina

# Verifica que las variables no sean None
if NOTION_TOKEN is None:
    raise ValueError("NOTION_API_TOKEN is not set in environment variables.")
if PARENT_PAGE_ID is None:
    raise ValueError("NOTION_PAGE_ID is not set in environment variables.")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Función para dividir el contenido en fragmentos de máximo 2000 caracteres
def split_content(content, max_length=2000):
    return [content[i:i+max_length] for i in range(0, len(content), max_length)]

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"page_id": PARENT_PAGE_ID},  # Aquí se usa el ID de la página, no de una base de datos
        "properties": data["properties"],
        "children": data.get("children", [])  # Incluye los bloques de contenido si están presentes
    }

    res = requests.post(create_url, headers=headers, json=payload)

    if res.status_code != 200:
        print(f"Error: {res.status_code} - {res.text}")
    return res


def append_to_page(page_id, content_blocks):
    """Añadir contenido a una página existente como varios bloques"""
    update_url = f"https://api.notion.com/v1/blocks/{page_id}/children"  # Ensure the correct page_id is used

    payload = {"children": content_blocks}
    print(content_blocks)

    res = requests.patch(update_url, headers=headers, json=payload)
    if res.status_code != 200:
        print(f"Error: {res.status_code} - {res.text}")
    else:
        print(f"Successfully added blocks to page {page_id}")


def create_debugging_page(title, content):
    """Crear una nueva página de debugging al inicio de la sesión"""
    try:
        # Construir el contenido para la subpágina de Notion
        page_data = {
            "properties": {
                "title": [  
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
        }

        create_url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"page_id": PARENT_PAGE_ID},  # Aquí se usa el ID de la página, no de una base de datos
            "properties": page_data["properties"],
            "children": page_data["children"]
        }

        response = requests.post(create_url, headers=headers, json=payload)
        if response.status_code == 200:
            page_id = response.json()["id"]
            print(f"Page '{title}' created in Notion with ID {page_id}")
            return page_id  # Devuelve el page_id para usarlo después
        else:
            print(f"Error creating page: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating page in Notion: {e}")
        return None


def add_debugging_content(page_id, command, output):
    """Add a command and its output to the Notion page as numbered list with nested code block"""
    try:
        # Create the numbered list item block for the command
        numbered_list_item_block = {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Command: {command}"
                        }
                    }
                ],
                "children": []
            }
        }

        # Split the output into multiple blocks if it's too large
        output_chunks = split_content(output)

        # Create a code block for each chunk of the output
        for chunk in output_chunks:
            code_block = {
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ],
                    "language": "bash"  # Set syntax highlighting for bash
                }
            }
            # Append each code block to the children of the numbered list item
            numbered_list_item_block["numbered_list_item"]["children"].append(code_block)

        # Append the numbered list item (with the nested code blocks) to the page
        append_to_page(page_id, [numbered_list_item_block])
        print(f"Command and output added to page with ID {page_id}")

    except Exception as e:
        print(f"Error adding content to Notion page: {e}")
