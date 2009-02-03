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

parent_id = "linkroll";
count = 5;

// Node between posts
make_post_delimiter = function()
{
    return document.createElement("br");
}

make_post_node = function(post)
{
    node = document.createElement("a")
    node.setAttribute("href", post.u);
    if (post.n)
        node.setAttribute("title", post.n);
    node.appendChild(document.createTextNode(post.d));
    return node;
}

delcb = function(post_list) 
{
    var parent = document.getElementById(parent_id);
    
    for (var i = 0; (i < count) && (p = post_list[i]); i++) {
        parent.appendChild(make_post_node(p));
        parent.appendChild(make_post_delimiter());
    }
}
