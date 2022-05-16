export function getFormDataFromObject(obj) {
    let formData = new FormData()

    for (const [key, value] of Object.entries(obj)) {
        //Check for array(file upload) and add the files to form body
        if(Array.isArray(value)) {
            value.forEach((fileItem) => {
                formData.append(key, fileItem.file)
              })
        } else {
            formData.append(key, value);
        }
    }
    return formData
}