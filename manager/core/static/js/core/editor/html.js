var edjsHTML=function(){"use strict";var e={delimiter:function(){return"<br/>"},header:function(e){var t=e.data;return"<h"+t.level+">"+t.text+"</h"+t.level+">"},paragraph:function(e){return"<p>"+e.data.text+"</p>"},list:function(e){var t=e.data,r="unordered"===t.style?"ul":"ol",n=function(e,t){var r=e.map((function(e){if(!e.content&&!e.items)return"<li>"+e+"</li>";var r="";return e.items&&(r=n(e.items,t)),e.content?"<li> "+e.content+" </li>"+r:void 0}));return"<"+t+">"+r.join("")+"</"+t+">"};return n(t.items,r)},image:function(e){var t=e.data,r=t.caption?t.caption:"Image";return'<img src="'+(t.file&&t.file.url?t.file.url:t.file)+'" alt="'+r+'" />'},quote:function(e){var t=e.data;return"<blockquote>"+t.text+"</blockquote> - "+t.caption},code:function(e){return"<pre><code>"+e.data.code+"</code></pre>"},embed:function(e){var t=e.data;switch(t.service){case"vimeo":return'<iframe src="'+t.embed+'" height="'+t.height+'" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>';case"youtube":return'<iframe width="'+t.width+'" height="'+t.height+'" src="'+t.embed+'" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';default:throw new Error("Only Youtube and Vime Embeds are supported right now.")}}};function t(e){return new Error('[31m The Parser function of type "'+e+'" is not defined. \n\n  Define your custom parser functions as: [34mhttps://github.com/pavittarx/editorjs-html#extend-for-custom-blocks [0m')}var r=function(n){void 0===n&&(n={});var i=Object.assign({},e,n);return{parse:function(e){return e.blocks.map((function(e){return i[e.type]?i[e.type](e):t(e.type)}))},parseBlock:function(e){return i[e.type]?i[e.type](e):t(e.type)},parseStrict:function(e){var n=e.blocks,o=r(i).validate({blocks:n});if(o.length)throw new Error("Parser Functions missing for blocks: "+o.toString());for(var a=[],u=0;u<n.length;u++){if(!i[n[u].type])throw t(n[u].type);a.push(i[n[u].type](n[u]))}return a},validate:function(e){var t=e.blocks.map((function(e){return e.type})).filter((function(e,t,r){return r.indexOf(e)===t})),r=Object.keys(i);return t.filter((function(e){return!r.includes(e)}))}}};return r}();
