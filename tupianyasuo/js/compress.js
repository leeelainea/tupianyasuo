class ImageCompressor {
    constructor() {
        this.maxWidth = 1920; // 最大宽度限制
        this.quality = 0.8; // 默认压缩质量
    }

    // 压缩图片
    async compress(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                const img = new Image();
                img.src = e.target.result;
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;

                    // 如果图片宽度超过限制，等比例缩小
                    if (width > this.maxWidth) {
                        height = Math.round((height * this.maxWidth) / width);
                        width = this.maxWidth;
                    }

                    canvas.width = width;
                    canvas.height = height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);

                    // 转换为 blob
                    canvas.toBlob(
                        (blob) => {
                            resolve({
                                blob,
                                width,
                                height,
                                originalSize: file.size,
                                compressedSize: blob.size
                            });
                        },
                        file.type,
                        this.quality
                    );
                };
                img.onerror = reject;
            };
            reader.onerror = reject;
        });
    }

    // 设置压缩质量
    setQuality(quality) {
        this.quality = quality / 100;
    }

    // 格式化文件大小
    static formatSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
} 