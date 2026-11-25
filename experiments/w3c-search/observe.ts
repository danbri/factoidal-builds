// Test-only paint markers preserve the live form's markup, dimensions and action.
// Observe the W3C response independently of the third-party search provider.
const originalFetch = globalThis.fetch;
const searchPage = "https://www.w3.org/help/search/";
globalThis.fetch = async (input, init) => {
  const url = new URL(input instanceof Request ? input.url : input);
  const response = await originalFetch(input, init);
  if (url.origin === "https://www.w3.org" && url.pathname === "/Help/search") {
    console.log(JSON.stringify({type: "w3c-search-handoff", url: url.href,
      status: response.status, location: response.headers.get("location")}));
  }
  if (url.origin === "https://duckduckgo.com" && url.pathname === "/" &&
      url.searchParams.get("q")?.startsWith("site:www.w3.org ")) {
    console.log(JSON.stringify({type: "w3c-search-provider", url: url.href, status: response.status}));
  }
  if (url.href !== searchPage || !response.ok) return response;
  const html = await response.text();
  const headers = new Headers(response.headers);
  headers.delete("content-length");
  headers.delete("content-encoding");
  const anchor = "</head>";
  if (!html.includes(anchor)) throw new Error("W3C search response has no head");
  const mark = '<style>#search{background-color:#c7e9cf!important} ' +
    'form[role=search] button[type=submit]{background-color:#d8d2f3!important}</style>';
  return new Response(html.replace(anchor, mark + anchor), {
    status: response.status, statusText: response.statusText, headers,
  });
};
