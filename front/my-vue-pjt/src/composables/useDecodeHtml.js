export function useDecodeHtml() {
    const decodeHtml = (html) => {
      const txt = document.createElement('textarea');
      txt.innerHTML = html;
      return txt.value;
    };
  
    return { decodeHtml };
  }
  