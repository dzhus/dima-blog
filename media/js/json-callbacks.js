/*
 * Del.icio.us and Flickr JSON feed entries using DOM
 *
 * This snippet provides `delcb` callback which should be used as
 * follows:
 *
 *     <script type="text/javascript"
 *             src="http://feeds.delicious.com/v2/json/SphinxTheGeek?count=15&amp;callback=delcb"></script>
 *
 * `flickcb` callback should be used with
 * `flickr.people.getPublicPhotos` method of Flickr API:
 *
 * 
 *
 * String variable `delicious_parent_id` is the id of DOM node to which entries
 * will be appended.
 *
 * `count` is the maximum entries count.
 *
 * No more options are supported yet.
 */

var flickr_parent_id = "flickr_photo";
var delicious_parent_id = "linkroll";
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
    var parent = document.getElementById(delicious_parent_id);
    
    for (var i = 0; p = post_list[i]; i++) {
        parent.appendChild(make_post_node(p));
        parent.appendChild(make_post_delimiter());
    }
}

make_photo_node = function(photo)
{
    var link = document.createElementNS(xhns, "a");
    link.setAttribute("href", "http://www.flickr.com/photos/" + photo.owner + "/" + photo.id);
    link.setAttribute("title", "Перейти на страницу фотографии «" + photo.title + "»");
    
    var img = document.createElementNS(xhns, "img");
    img.setAttribute("src", "http://farm" + photo.farm + ".static.flickr.com/" + 
                     photo.server + "/" + photo.id + "_" + photo.secret + "_z.jpg");
    img.setAttribute("alt", photo.title);
    link.appendChild(img);
    return link;
}

flickcb = function(photo_list)
{
    var parent = document.getElementById(flickr_parent_id);
    
    for (var i = 0; p = photo_list.photos.photo[i]; i++)
        parent.appendChild(make_photo_node(p));
}
