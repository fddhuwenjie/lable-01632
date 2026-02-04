"""
RSA 加密模块 - 用于密码传输加密
"""
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

# 生成 RSA 密钥对（应用启动时生成，内存中保存）
_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
_public_key = _private_key.public_key()


def get_public_key_pem() -> str:
    """获取 PEM 格式的公钥"""
    pem = _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')


def decrypt_password(encrypted_password: str) -> str:
    """
    解密前端加密的密码
    
    Args:
        encrypted_password: Base64 编码的加密密码
        
    Returns:
        解密后的明文密码
    """
    try:
        encrypted_bytes = base64.b64decode(encrypted_password)
        decrypted_bytes = _private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"密码解密失败: {str(e)}")
