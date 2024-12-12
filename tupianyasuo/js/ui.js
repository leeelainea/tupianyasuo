document.addEventListener('DOMContentLoaded', () => {
    const compressor = new ImageCompressor();
    let currentFile = null;

    // DOM 元素
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const previewArea = document.getElementById('previewArea');
    const originalImage = document.getElementById('originalImage');
    const compressedImage = document.getElementById('compressedImage');
    const originalSize = document.getElementById('originalSize');
    const compressedSize = document.getElementById('compressedSize');
    const originalDimensions = document.getElementById('originalDimensions');
    const compressionRatio = document.getElementById('compressionRatio');
    const qualitySlider = document.getElementById('qualitySlider');
    const qualityValue = document.getElementById('qualityValue');
    const downloadBtn = document.getElementById('downloadBtn');

    // 事件监听
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    qualitySlider.addEventListener('input', (e) => {
        qualityValue.textContent = e.target.value + '%';
        if (currentFile) {
            compressor.setQuality(e.target.value);
            compressImage(currentFile);
        }
    });

    downloadBtn.addEventListener('click', () => {
        if (compressedImage.src) {
            const link = document.createElement('a');
            link.download = 'compressed-image.' + currentFile.name.split('.').pop();
            link.href = compressedImage.src;
            link.click();
        }
    });

    // 处理文件
    async function handleFiles(files) {
        const file = files[0];
        if (file && file.type.startsWith('image/')) {
            currentFile = file;
            previewArea.hidden = false;
            displayOriginalImage(file);
            await compressImage(file);
        }
    }

    // 显示原图
    function displayOriginalImage(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
            originalSize.textContent = ImageCompressor.formatSize(file.size);
        };
        reader.readAsDataURL(file);
    }

    // 压缩图片
    async function compressImage(file) {
        try {
            const result = await compressor.compress(file);
            compressedImage.src = URL.createObjectURL(result.blob);
            compressedSize.textContent = ImageCompressor.formatSize(result.compressedSize);
            originalDimensions.textContent = `${result.width} x ${result.height}`;
            
            const ratio = ((1 - result.compressedSize / result.originalSize) * 100).toFixed(1);
            compressionRatio.textContent = ratio + '%';
        } catch (error) {
            console.error('压缩失败:', error);
        }
    }
}); 