
PlatformCode ={
    "0": "Windows",
    "1": "iOS",
    "2": "Android",
    "3": "MacOs",
    "4": "Linux",
    "5": "other",
    "Windows": 0,
    "iOS": 1,
    "Android": 2,
    "MacOs": 3,
    "Linux": 4,
    "other": 5
}
function getPlatformCode(e) {
    switch (e) {
    case "Android":
        return PlatformCode.Android;
    case "iOS":
        return PlatformCode.iOS;
    case "Mac OS":
        return PlatformCode.MacOs;
    case "Linux":
        return PlatformCode.Linux;
    default:
        return PlatformCode.other
    }
}
var CHARSET = "abcdefghijklmnopqrstuvwxyz1234567890", PlatformCode;
function genRandomString(e) {
    // 创建一个长度为 e 的数组，并用 undefined 填充
    var r = new Array(e).fill(void 0);

    // 使用 map 方法来替换每个元素，使用 CHARSET 中的随机字符替换
    var t = r.map(function() {
        return CHARSET[Math.floor(36 * Math.random())];
    });

    return t.join('');
}
var crc32 = function(e) {
    for (var t, r = [], n = 0; n < 256; n++) {
        t = n;
        for (var o = 0; o < 8; o++)
            t = 1 & t ? 3988292384 ^ t >>> 1 : t >>> 1;
        r[n] = t
    }
    for (var i = -1, a = 0; a < e.length; a++)
        i = i >>> 8 ^ r[255 & (i ^ e.charCodeAt(a))];
    return ~i >>> 0
};
function generateLocalId(e) {
    var a = getPlatformCode(e);
    var o = "".concat((+new Date).toString(16));
    var n = o + genRandomString(30);
    var r = n + a;
    var t = r + "0";
    var s = t + "000";
    var u = crc32(s);
    var i = s + u;
    return i.substring(0, 52);
}
function a1(){
    for (var c = "", l = 0; l < 1e3 && 52 !== c.length; )
        c = generateLocalId('Windows'),
        l++;
return c}

function read(e) {
    return '"' === e[0] && (e = e.slice(1, -1)),
    e.replace(/(%[\dA-F]{2})+/gi, decodeURIComponent)
}
function write(e) {
    return encodeURIComponent(e).replace(/%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g, decodeURIComponent)
}
console.log(a1().length);