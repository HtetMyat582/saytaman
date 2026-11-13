// Photo Compressor
(() => {
    const MAX_DIMENSION = 1920;
    const MAX_JPEG_BYTES = 1.5 * 1024 * 1024;
    const processedFiles = new WeakSet();
    const pending = new WeakMap();

    function canvasBlob(canvas, type, quality) {
        return new Promise((resolve, reject) => {
            canvas.toBlob(
                blob => blob ? resolve(blob) : reject(new Error("Image compression failed.")),
                type,
                quality
            );
        });
    }

    async function compressInput(input) {
        if (pending.has(input)) {
            return pending.get(input);
        }

        const operation = (async () => {
            const original = input.files?.[0];

            if (
                !original ||
                processedFiles.has(original) ||
                !["image/jpeg", "image/png"].includes(original.type)
            ) {
                return;
            }

            let bitmap;
            try {
                bitmap = await createImageBitmap(original);

                const largestSide = Math.max(bitmap.width, bitmap.height);
                const scale = Math.min(1, MAX_DIMENSION / largestSide);
                let width = Math.max(1, Math.round(bitmap.width * scale));
                let height = Math.max(1, Math.round(bitmap.height * scale));

                const canvas = document.createElement("canvas");
                const isJpeg = original.type === "image/jpeg";
                let blob;

                for (let attempt = 0; attempt < 5; attempt++) {
                    canvas.width = width;
                    canvas.height = height;

                    const context = canvas.getContext("2d");
                    if (!context) return;

                    if (isJpeg) {
                        context.fillStyle = "#fff";
                        context.fillRect(0, 0, width, height);
                    }
                    context.drawImage(bitmap, 0, 0, width, height);

                    blob = await canvasBlob(
                        canvas,
                        original.type,
                        isJpeg ? Math.max(0.58, 0.82 - attempt * 0.08) : undefined
                    );

                    if (!isJpeg || blob.size <= MAX_JPEG_BYTES) break;

                    width = Math.max(1, Math.round(width * 0.85));
                    height = Math.max(1, Math.round(height * 0.85));
                }

                if (!blob || blob.size >= original.size) return;

                const extension = isJpeg ? ".jpg" : ".png";
                const filename = original.name.replace(/\.[^.]+$/, "") + extension;
                const compressed = new File([blob], filename, {
                    type: blob.type,
                    lastModified: original.lastModified
                });

                const transfer = new DataTransfer();
                transfer.items.add(compressed);
                input.files = transfer.files;
                processedFiles.add(compressed);
            } catch {
                // Leave the original file selected if the browser cannot process it.
            } finally {
                bitmap?.close();
            }
        })();

        pending.set(input, operation);
        try {
            await operation;
        } finally {
            pending.delete(input);
        }
    }

    [...document.querySelectorAll('form[enctype="multipart/form-data"]')]
        .filter(form => form.querySelector('#photo-formset-container'))
        .forEach(form => {
            const imageInputs = () => [...form.querySelectorAll('input[type="file"]')];

        form.addEventListener("change", event => {
            if (event.target.matches('input[type="file"]')) {
                void compressInput(event.target);
            }
        });

        let resubmitting = false;
        form.addEventListener("submit", async event => {
            if (resubmitting) return;

            event.preventDefault();
            await Promise.all(imageInputs().map(compressInput));

            resubmitting = true;
            if (form.requestSubmit) {
                form.requestSubmit(event.submitter);
            } else {
                form.submit();
            }
        });
    });
})();