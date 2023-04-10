var proxyconf = {
    mode: "pac_script",
    pacScript: {
        data: 'function FindProxyForURL(url, host) {\n' +
            '    var twitch = ["twitch.tv", "usher.ttvnw.net", "abs.hls.ttvnw.net", "assets.clips.twitchcdn.net"]\n' +
            '    var cloudfront = ["d2e2de1etea730.cloudfront.net", "dqrpb9wgowsf5.cloudfront.net", "ds0h3roq6wcgc.cloudfront.net", "d2nvs31859zcd8.cloudfront.net", "d2aba1wr3818hz.cloudfront.net", "d3c27h4odz752x.cloudfront.net", "dgeft87wbj63p.cloudfront.net", "d1m7jfoe9zdc1j.cloudfront.net", "d3vd9lfkzbru3h.cloudfront.net", "d2vjef5jvl6bfs.cloudfront.net", "d1ymi26ma8va5x.cloudfront.net", "d1mhjrowxxagfy.cloudfront.net", "ddacn6pr5v0tl.cloudfront.net", "d3aqoihi2n8ty8.cloudfront.net"]\n' +
            '    for (var i = 0; i < twitch.length; i++)\n' +
            '        if (host.includes(twitch[i])) \n' +
            '            return "HTTPS proxy2.ontdb.com:5000";\n' +
            '    for (var i = 0; i < cloudfront.length; i++)\n' +
            '        if (host.includes(cloudfront[i])) \n' +
            '            return "HTTPS proxy2.ontdb.com:5000";\n' +
            '}\n'
    }
}
chrome.proxy.settings.set({ value: proxyconf, scope: 'regular' }, function () { });