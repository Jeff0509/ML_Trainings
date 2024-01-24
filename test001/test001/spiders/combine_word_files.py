import os
from docx import Document

# Specify the directory where the downloaded Word files are located
downloaded_files_dir = 'downloaded_files'

# Specify the prefix for the combined Word documents
combined_docx_prefix = 'combined_word_doc_'

# Maximum allowed file size in bytes (250KB)
max_file_size_bytes = 250 * 1024

def combine_word_files(directory, output_prefix, files_per_group=800):
    # Get a list of all .docx files in the directory
    docx_files = [f for f in os.listdir(directory) if f.endswith('.docx')]
    
    # Divide the files into groups
    file_groups = [docx_files[i:i + files_per_group] for i in range(0, len(docx_files), files_per_group)]

    for group_index, file_group in enumerate(file_groups):
        combined_doc = Document()
        output_file = f"{output_prefix}{group_index}.docx"

        for docx_file in file_group:
            file_path = os.path.join(directory, docx_file)

            # Check the file size before opening
            file_size = os.path.getsize(file_path)

            if file_size <= max_file_size_bytes:
                # Open each downloaded Word file
                doc = Document(file_path)

                # Add the content of the Word file to the combined document
                for element in doc.element.body:
                    combined_doc.element.body.append(element)

        # Save the combined document for this group to the specified output file
        combined_doc.save(output_file)
        print(f"Combined Word document '{output_file}' created.")

if __name__ == "__main__":
    combine_word_files(downloaded_files_dir, combined_docx_prefix)
