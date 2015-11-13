function init(block, value){
  block.css("background","white");
  block.attr("id",value.image_id);
  block.find("button").html(value.status);
  block.find("img").attr("src", value.image_path);
  if(value.status == "unlabelled"){
    addUnlabel(block);
  }
  else{
    addStatus(block, value.status);
  }

}

function addChoose(block){
  block.addClass("on");
  block.css("background","yellow");
}
function removeChoose(block){
    block.removeClass("on");
    block.css("background","white");
}
// function addalready(block){
//     block.removeClass("on");
//     block.addClass("already");
//     block.css("background","MediumSeaGreen");
// }
function addStatus(block,status){
  if(status.indexOf("positive") > -1){
    addPositive(block);
  }
  else if(status.indexOf("negative") > -1){
    addNegative(block);
  }
  else if(status.indexOf("uncertain") > -1){
    addUncertain(block);
  }
}

function addUnlabel(block){
  block.removeClass("on");
  block.css("background","white");
}
function addPositive(block){
  block.removeClass("on");
  block.css("background","MediumSeaGreen");
}
function addNegative(block){
  block.removeClass("on");
  block.css("background","chocolate");
}
function addUncertain(block){
  block.removeClass("on");
  block.css("background","royalblue");
}

function prompt(){
  var name=prompt("input a username","lcy4869@qq.com");
  // alert("hello");
}
