if (!Date.prototype.toISOString) {
    Date.prototype.toISOString = function () {
        function pad(n) { return n < 10 ? '0' + n : n; }
        function ms(n) { return n < 10 ? '00'+ n : n < 100 ? '0' + n : n }
        return this.getFullYear() + '-' +
            pad(this.getMonth() + 1) + '-' +
            pad(this.getDate()) + 'T' +
            pad(this.getHours()) + ':' +
            pad(this.getMinutes()) + ':' +
            pad(this.getSeconds()) + '.' +
            ms(this.getMilliseconds()) + 'Z';
    }
}

function createHAR(address, title, startTime, resources)
{
    var entries = [];

    resources.forEach(function (resource) {
        var request = resource.request,
            startReply = resource.startReply,
            endReply = resource.endReply;

        if (!request) {
            return;
        }

        // Exclude Data URI from HAR file because
        // they aren't included in specification
        if (request.url.match(/(^data:image\/.*)/i)) {
            return;
	}

        entries.push({
            startedDateTime: request.time.toISOString(),
            time: resource.endTime - request.time,
            request: {
                method: request.method,
                url: request.url,
                httpVersion: "HTTP/1.1",
                cookies: [],
                headers: request.headers,
                queryString: [],
                headersSize: -1,
                bodySize: -1
            },
            response: {
                status: resource.status,
                statusText: resource.status,
                httpVersion: "HTTP/1.1",
                cookies: [],
                headers: endReply && endReply.headers || "",
                redirectURL: "",
                headersSize: -1,
                bodySize: resource.responseBodySize,
                content: {
                    size: resource.responseBodySize,
                    mimeType: endReply && endReply.contentType || ""
                }
            },
            cache: {},
            timings: {
                blocked: 0,
                dns: -1,
                connect: -1,
                send: 0,
                wait: 0,
                receive: 0,
                ssl: -1
            },
            pageref: address
        });
    });

    return {
        log: {
            version: '1.2',
            creator: {
                name: "PhantomJS",
                version: phantom.version.major + '.' + phantom.version.minor +
                    '.' + phantom.version.patch
            },
            pages: [{
                startedDateTime: startTime.toISOString(),
                id: address,
                title: title,
                pageTimings: {
                    onLoad: page.endTime - page.startTime
                }
            }],
            entries: entries
        }
    };
}

var page = require('webpage').create(),
    system = require('system');
    page.settings.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1';

if (system.args.length === 1) {
    console.log('Usage: netsniff.js <some URL>');
    phantom.exit(1);
} else {

    page.address = system.args[1];
    page.resources = [];

    page.onLoadStarted = function () {
        page.startTime = new Date();
    };

    page.onResourceRequested = function (req) {
        page.resources[req.id] = {
            request: req,
            startReply: null,
            endReply: null,
            responseBodySize: 0,
            status: 0,
            endTime: 0
        };
    };

    page.onResourceReceived = function (res) {
        if (res.stage === 'start') {
            page.resources[res.id].startReply = res;
        }
        if (res.stage === 'end') {
            page.resources[res.id].endReply = res;
            page.resources[res.id].endTime = res.time;
            page.resources[res.id].status = res.status;
        }
        if(res.bodySize){
            page.resources[res.id].responseBodySize += res.bodySize;
        }
    };

    page.onResourceTimeout = function (res) {
        page.resources[res.id].endTime = new Date();
        page.resources[res.id].status = res.errorCode;
    };

    page.onResourceError = function (res) {
        page.resources[res.id].endTime = new Date();
        page.resources[res.id].status = res.errorCode;
    };

    var loadCount = 0;
    var finalHar = [];
    var docContent = "";

    function loadCallback(status) {
        loadCount ++;
        if(loadCount == 1){
            docContent = page.content;
        }
        var har;
        if (status !== 'success') {
            console.log('FAIL to load the address');
            phantom.exit(1);
        } else {
            page.endTime = new Date();
            page.title = page.evaluate(function () {
                return document.title;
            });
            har = createHAR(page.address, page.title, page.startTime, page.resources);
            finalHar.push(har);
            if(loadCount==2){
                console.log('xafexdfea980!adaf*>M')
                var result = {
                    content: docContent,
                    hars: finalHar
                };
                console.log(JSON.stringify(result, undefined, 4));
                phantom.exit(1);
            }else{
                page.resources = [];
                page.open(page.address, loadCallback);
            }
        }
    }

    page.open(page.address, loadCallback);
}
