// Eleventy config - Central de Ajuda Nexus
// Le paginas e Markdowns da raiz do projeto e gera o site final em _site/.
// Cloudflare Pages publica o conteudo dessa pasta automaticamente.

module.exports = function (eleventyConfig) {

  // Pastas e arquivos copiados direto para o output (sem processar)
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("modulos/*.html");
  eleventyConfig.addPassthroughCopy("index.html");
  eleventyConfig.addPassthroughCopy("modulos.html");
  eleventyConfig.addPassthroughCopy("_redirects");

  // Colecoes de conteudo (geridas pelo Decap CMS)
  eleventyConfig.addCollection("faqs", function (api) {
    return api.getFilteredByGlob("_content/faqs/*.md");
  });

  eleventyConfig.addCollection("noticias", function (api) {
    return api.getFilteredByGlob("_content/noticias/*.md")
      .sort(function (a, b) { return new Date(b.data.date) - new Date(a.data.date); });
  });

  eleventyConfig.addCollection("artigos", function (api) {
    return api.getFilteredByGlob("_content/artigos/*.md");
  });

  eleventyConfig.addCollection("videos", function (api) {
    return api.getFilteredByGlob("_content/videos/*.md");
  });

  // Filtro de data em portugues: "22 de maio de 2026"
  eleventyConfig.addFilter("dataPtBr", function (data) {
    if (!data) return "";
    var d = new Date(data);
    var meses = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho",
                 "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
    return d.getUTCDate() + " de " + meses[d.getUTCMonth()] + " de " + d.getUTCFullYear();
  });

  // Extrai o ID de uma URL do YouTube
  eleventyConfig.addFilter("youtubeId", function (url) {
    if (!url) return "";
    var m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : "";
  });

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["njk", "md"]
  };
};
