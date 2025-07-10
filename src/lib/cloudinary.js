// Configuração do Cloudinary
const CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/dira0n0ic/image/upload'
const CLOUDINARY_UPLOAD_PRESET = 'tribodocerrado' // Você precisa criar este preset no Cloudinary

export const uploadImageToCloudinary = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET)
  formData.append('cloud_name', 'dira0n0ic')

  try {
    const response = await fetch(CLOUDINARY_URL, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Erro no upload da imagem')
    }

    const data = await response.json()
    return {
      success: true,
      url: data.secure_url,
      publicId: data.public_id
    }
  } catch (error) {
    console.error('Erro no upload:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

export const getOptimizedImageUrl = (publicId, options = {}) => {
  const {
    width = 400,
    height = 400,
    crop = 'fill',
    quality = 'auto',
    format = 'auto'
  } = options

  return `https://res.cloudinary.com/dira0n0ic/image/upload/w_${width},h_${height},c_${crop},q_${quality},f_${format}/${publicId}`
}

