/**
 * RSA 加密工具 - 用于密码加密传输
 */

let cachedPublicKey: string | null = null

/**
 * 获取服务器公钥
 */
export async function getPublicKey(): Promise<string> {
  if (cachedPublicKey) {
    return cachedPublicKey
  }
  
  const response = await fetch('/api/auth/public-key')
  const data = await response.json()
  cachedPublicKey = data.public_key
  return cachedPublicKey!
}

/**
 * 将 PEM 格式公钥转换为 CryptoKey
 */
async function importPublicKey(pem: string): Promise<CryptoKey> {
  // 移除 PEM 头尾和换行
  const pemContents = pem
    .replace('-----BEGIN PUBLIC KEY-----', '')
    .replace('-----END PUBLIC KEY-----', '')
    .replace(/\s/g, '')
  
  // Base64 解码
  const binaryString = atob(pemContents)
  const bytes = new Uint8Array(binaryString.length)
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i)
  }
  
  // 导入公钥
  return await crypto.subtle.importKey(
    'spki',
    bytes.buffer,
    {
      name: 'RSA-OAEP',
      hash: 'SHA-256'
    },
    false,
    ['encrypt']
  )
}

/**
 * 使用 RSA 公钥加密密码
 */
export async function encryptPassword(password: string): Promise<string> {
  const publicKeyPem = await getPublicKey()
  const publicKey = await importPublicKey(publicKeyPem)
  
  // 将密码转换为 ArrayBuffer
  const encoder = new TextEncoder()
  const data = encoder.encode(password)
  
  // 加密
  const encrypted = await crypto.subtle.encrypt(
    { name: 'RSA-OAEP' },
    publicKey,
    data
  )
  
  // 转换为 Base64
  const bytes = new Uint8Array(encrypted)
  let binary = ''
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i])
  }
  return btoa(binary)
}
