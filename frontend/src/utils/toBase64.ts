export const toBase64 = (file: File) =>
    new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve((reader.result as string)?.replace('data:image/jpeg;base64,', ''));
        reader.onerror = reject;
    });
