var duration={};
var positions=[];
var rawData=null;
var depthData=null;
var flowData=null;
var depthAnimationData=null;
var maxAnimationData=-1.0;
var minAnimationData=100000000.0;
var currentAnimationTime=0;
var animationDuration=10.0;
var timer=null;
$(function() {

initialiseElements();
//refreshGraph();

});
function initialiseElements(){
	// Add the Flot version string to the footer
	$("#footer").prepend("Hydro Tools v1.0 Flot " + $.plot.version + " &ndash;");
   $("#animate").click(animate)
   $("#btn_start").on('click',startSim);
   $('#graphType').change(displaySelectedGraph);
}
function animate(){
   $("#btn_start").attr("disabled", true);
   currentAnimationTime=0;
   var numTimes = parseFloat(depthAnimationData.length);
   var interval =  animationDuration*1000.0/numTimes;
   timer=setInterval(showAnimation, interval)
}
function showAnimation(){

   var xaxis= {
      axisLabel: 'Position Along Channel',
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 10,
      axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
      axisLabelPadding: 10
  }
  var yaxis= {
   min:minAnimationData,
   max:maxAnimationData};
   var options = {xaxis:xaxis, yaxis:yaxis};
   updateCurrentTime(currentAnimationTime);
   $.plot("#placeholder", [depthAnimationData[currentAnimationTime]], options);
   currentAnimationTime++;
   if (currentAnimationTime>=depthAnimationData.length){
      clearInterval(timer);
      $("#btn_start").attr("disabled", false);
   }
}

function displaySelectedGraph(){
 	var graph =$('#graphType').val();
   displayGraph([depthData[graph], flowData[graph]]);
   updateCurrentTime("-");                        
}
function updateCurrentTime(secs){
    $("#current").val(secs);
}

function startSim(){
        var data = {}
        data.config = {}
        data.config.upstream = {}
        data.config.downstream = {}
        data.config.shape=parseInt($('#shape').val());
        data.config.width=parseFloat($('#width').val());
        data.config.length=parseFloat($('#length').val());
        data.config.manning=parseFloat($('#manning').val());
        data.config.slope=parseFloat($('#slope').val());
        data.config.qinit=parseFloat($('#qinit').val());
        data.config.reaches=parseFloat($('#reaches').val());
        data.config.iterations=parseFloat($('#iterations').val());
        data.config.upstream.type=parseInt($('#utype').val());
        data.config.upstream.rate=parseFloat($('#urate').val());
        data.config.upstream.final=parseFloat($('#ufinal').val());
        data.config.downstream.type=parseInt($('#dtype').val());
        data.config.downstream.rate=parseFloat($('#drate').val());
        data.config.downstream.final=parseFloat($('#dfinal').val());
        $.ajax({url:"rest/ocusf", type: "POST",data: JSON.stringify(data),
                dataType: 'json',
                contentType: 'application/json',
                success:gotGraphData});
}

function gotGraphData(data){
        rawData=data;
        processData(data);
        populateDropDown();
	     displaySelectedGraph();
}
function populateDropDown(){
    $('#graphType').children().remove();
    for (var i=0;i<positions.length;i++){
        var itemval= '<option value="' + i +'">' + positions[i].name + '</option>';
       $("#graphType").append(itemval);
    }
}
function displayGraph(data){
   var xaxis= {
      axisLabel: 'Time (Seconds)',
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 10,
      axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
      axisLabelPadding: 10
  }
   var options = {xaxis:xaxis};
   $.plot("#placeholder", data, options);
}

function processData(data){
    var tm =0;
    var obj = data;
    //Populate list of known positions
    getPositionsList(obj.results);
    initGraphData(obj.results.length);
    $.each(obj.results,function(index,item){
        if(item.hasOwnProperty('data') && item.hasOwnProperty('secs')){
           for(var i=0;i<item.data.length;i++){
            if(item.data[i].hasOwnProperty('pos') && item.data[i].hasOwnProperty('q') && item.data[i].hasOwnProperty('d')){
              var idx =  getGraphIndex(item.data[i].pos);
              var x = parseFloat(item.data[i].pos.substring(0,4));
               depthData[idx].data.push([item.secs,item.data[i].d]);
               flowData[idx].data.push([item.secs,item.data[i].q]);
               depthAnimationData[tm].data.push([x,item.data[i].d])
               if (item.data[i].d > maxAnimationData) maxAnimationData=item.data[i].d;
               if (item.data[i].d < minAnimationData) minAnimationData=item.data[i].d;
              }//end else
           }//end for positions
         }//end if   
         tm++;       
    });
      
}
function initGraphData(numTms){
   depthData=[];
   flowData=[];
   depthAnimationData=[];
   maxAnimationData=-1.0;
   minAnimationData=100000000.0;
   for (var i=0;i<positions.length;i++){
        depthData.push({data:[], label: positions[i].name + " Depth(m)" , duration:0});
        flowData.push({data:[], label: positions[i].name + " Flow(m3/s)" , duration:0});     
   }
   for (var j=0;j<numTms;j++){
      depthAnimationData.push({data:[], label: "Depth(m)" , duration:0});    
   }
}
function getGraphIndex(name){
   for (var i=0;i<depthData.length;i++){
      if(depthData[i].label.startsWith(name)){
         return i
      }
   }
   return -1
}
function getPositionsList(data){
    positions=[];
    for(var j=0;j<data.length;j++){
       item = data[j];
       if(item.hasOwnProperty('data')){
         //Only worth looking at first data records
         for(var i=0;i<item.data.length;i++){
            var row=item['data'][i];
            if (row.hasOwnProperty("pos")) {
               positions.push({'id':row['pos'],'name':row['pos']});    
            }//end if
         }//end for
         //Return after first record
         return;
      }//end if               
    };   
}
