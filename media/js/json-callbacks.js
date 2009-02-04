/*
 * Del.icio.us JSON feed entries using DOM
 *
 * This snippet provides `delcb` callback which should be used as
 * follows:
 *
 *     <script type="text/javascript"
 *             src="http://feeds.delicious.com/v2/json/SphinxTheGeek?count=15&amp;callback=delcb"></script>
 *
 * String variable `parent_id` is the id of DOM node to which entries
 * will be appended.
 *
 * `count` is the maximum entries count.
 *
 * No more options are supported yet.
 */

var parent_id = "linkroll";
var xhns = "http://www.w3.org/1999/xhtml";

make_post_delimiter = function()
{
    return document.createElementNS(xhns, "br");
}

make_post_node = function(post)
{
    // See <https://bugzilla.mozilla.org/show_bug.cgi?id=304713>
    var node = document.createElementNS(xhns, "a");
    node.setAttribute("href", post.u);
    if (post.n)
        node.setAttribute("title", post.n);
    node.appendChild(document.createTextNode(post.d));
    return node;
}

delcb = function(post_list) 
{
    var parent = document.getElementById(parent_id);
    
    for (var i = 0; p = post_list[i]; i++) {
        parent.appendChild(make_post_node(p));
        parent.appendChild(make_post_delimiter());
    }
}
