var proxyconf = {
    mode: "pac_script",
    pacScript: {
        data: "function FindProxyForURL(url, host) {\n" +
              "    if (host == 'gql.twitch.tv') \n" +
              "        return 'PROXY proxy2.ontdb.com:5000';\n" +
              "    else if (host.includes('cloudfront.net')) \n" +
              "        return 'PROXY proxy2.ontdb.com:5000';\n" +
              "    else if (host.includes('usher.ttvnw.net')) \n" +
              "        return 'PROXY proxy2.ontdb.com:5000';\n" +
              //"    }\n" +
              "}\n"
    }
}
chrome.proxy.settings.set({value: proxyconf, scope: 'regular'}, function() {});