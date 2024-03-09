import os
import shutil
import markdown

def create_markdown_file(title, path, content, metadata):
   # Create the markdown file
   with open(os.path.join(path, f"{title}.md"), "w") as f:
       # Write the metadata
       for k, v in metadata.items():
           f.write(f"{k}: {v}\n")
       f.write("\n")
       # Write the content
       f.write(content)

def import_image(src_path, dst_path):
   # Check if the destination directory exists, if not create it
   if not os.path.exists(dst_path):
       os.makedirs(dst_path)
   # Copy the image to the destination directory
   shutil.copy(src_path, dst_path)

# Example usage
create_markdown_file(
   "Espanol Mural",
   "/path/to/your/directory",
   "# Espanol Mural\nSome content here.",
   {
       "title": "Espanol Mural",
       "published": "2022-10-12",
       "cat": "Piece",
       "desc": "0.25 x 1.3 m",
       "cover": "espadon-mural.jpg"
   }
)

import_image("/path/to/source/image.jpg", "/path/to/destination/directory")
