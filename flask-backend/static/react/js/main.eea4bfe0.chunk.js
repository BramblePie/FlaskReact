(this["webpackJsonpreact-app"]=this["webpackJsonpreact-app"]||[]).push([[0],[,,,,function(e,t,n){e.exports=n.p+"media/logo.5d5d9eef.svg"},function(e,t,n){e.exports=n(13)},,,,,function(e,t,n){},function(e,t,n){},function(e,t,n){},function(e,t,n){"use strict";n.r(t);var a=n(0),c=n.n(a),o=n(3),r=n.n(o),l=(n(10),n(1)),i=n(4),u=n.n(i);n(11),n(12);var s=function(){return c.a.createElement("div",null,c.a.createElement("h2",null,"TESTING"))};var m=function(){var e=Object(a.useState)(new Date),t=Object(l.a)(e,2),n=t[0],o=t[1];return setInterval((function(){return o(new Date)}),1e3),c.a.createElement("div",null,c.a.createElement("h2",null,n.toLocaleTimeString()))};var p=function(){var e=Object(a.useState)(0),t=Object(l.a)(e,2),n=t[0],o=t[1],r=Object(a.useState)(0),i=Object(l.a)(r,2),p=i[0],d=i[1];return Object(a.useEffect)((function(){fetch("http://127.0.0.1/api/number/".concat(n)).then((function(e){return e.json()})).then((function(e){console.log(e),console.log(e[n]),d(e[n])}))}),[n]),c.a.createElement("div",{className:"App"},c.a.createElement("header",{className:"App-header"},c.a.createElement(m,null),c.a.createElement("img",{src:u.a,className:"App-logo",alt:"logo"}),c.a.createElement("p",null,"Edit ",c.a.createElement("code",null,"src/App.js")," and save to reload."),c.a.createElement("button",{onClick:function(){return o(n+1)}},"Clicked ",n," times"),c.a.createElement("p",{style:{color:p%2==0?"#800080":"#FFFFFF"}},p),c.a.createElement(s,null)))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(c.a.createElement(c.a.StrictMode,null,c.a.createElement(p,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}],[[5,1,2]]]);
//# sourceMappingURL=main.eea4bfe0.chunk.js.map