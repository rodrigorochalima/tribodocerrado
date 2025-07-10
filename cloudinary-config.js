// Configuração da API Cloudinary
const CLOUDINARY_CONFIG = {
    cloudName: 'dira0n0ic',
    apiKey: '286686119585265',
    apiSecret: 'hkvzCf2r4e84-dk7vPoK9dR-8B4',
    uploadPreset: 'tribodocerrado_uploads' // Será criado no painel Cloudinary
};

// Função para upload de imagem para Cloudinary
async function uploadImageToCloudinary(file) {
    try {
        console.log('📸 Iniciando upload para Cloudinary...');
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('upload_preset', 'ml_default'); // Usando preset padrão
        formData.append('cloud_name', CLOUDINARY_CONFIG.cloudName);
        
        const response = await fetch(`https://api.cloudinary.com/v1_1/${CLOUDINARY_CONFIG.cloudName}/image/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Upload bem-sucedido:', result);
        
        return {
            success: true,
            url: result.secure_url,
            publicId: result.public_id,
            width: result.width,
            height: result.height
        };
        
    } catch (error) {
        console.error('❌ Erro no upload:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Função para redimensionar imagem antes do upload
function resizeImage(file, maxWidth = 800, maxHeight = 600, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calcular novas dimensões mantendo proporção
            let { width, height } = img;
            
            if (width > height) {
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
            } else {
                if (height > maxHeight) {
                    width = (width * maxHeight) / height;
                    height = maxHeight;
                }
            }
            
            canvas.width = width;
            canvas.height = height;
            
            // Desenhar imagem redimensionada
            ctx.drawImage(img, 0, 0, width, height);
            
            // Converter para blob
            canvas.toBlob(resolve, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Função para validar arquivo de imagem
function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (!allowedTypes.includes(file.type)) {
        return {
            valid: false,
            error: 'Tipo de arquivo não suportado. Use: JPG, PNG, GIF ou WebP'
        };
    }
    
    if (file.size > maxSize) {
        return {
            valid: false,
            error: 'Arquivo muito grande. Máximo: 10MB'
        };
    }
    
    return { valid: true };
}

// Função para criar preview da imagem
function createImagePreview(file, previewElement) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        previewElement.src = e.target.result;
        previewElement.style.display = 'block';
    };
    
    reader.readAsDataURL(file);
}

console.log('📸 Cloudinary configurado para:', CLOUDINARY_CONFIG.cloudName);

