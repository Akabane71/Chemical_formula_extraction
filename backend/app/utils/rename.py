import uuid



def get_new_filename(original_filename: str) -> str:
    """
    生产一个新的文件名格式为: {original_filename}_{uuid}_{ext}
    """
    
    new_filename = f"{original_filename.split('.')[0]}_{uuid.uuid4()}.{original_filename.split('.')[-1]}"
    return new_filename

