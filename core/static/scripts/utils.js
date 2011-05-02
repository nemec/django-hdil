function newImage(liked){
  var oldFilename = document.getElementById("pic").src.replace(/^.*\/ /, '').replace(/^.*\\/, '');
  if (window.XMLHttpRequest){
    xmlhttp=new XMLHttpRequest();
  }
  else{
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function(){
    if(xmlhttp.readyState==4){
      if(xmlhttp.responseXML){
        var votecount = xmlhttp.responseXML.getElementsByTagName("votecount")[0].childNodes[0].nodeValue;
        document.getElementById("votebox").innerHTML=votecount;
        var filename = xmlhttp.responseXML.getElementsByTagName("filename")[0].childNodes[0].nodeValue;
        document.getElementById("pic").src=imagepath+filename;
      }
    }
  }
  if(liked == undefined){
    xmlhttp.open("GET","vote",true);
  }
  else{
    xmlhttp.open("GET","vote?liked="+liked+"&img="+oldFilename,true);
  }
  xmlhttp.send();
}
