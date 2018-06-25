function upload(page_cnt,id,language,source_db,title,isoa,type,resourceType){
/*	var user = $("#user").val();
	if(user == "{}"){
		getloginurl("ALL");
	}else{*/
		title=window.encodeURI(window.encodeURI(title));
		var type = $("#document_type").val();
		if(type == "standards"){
			type="standard";
		}
		window.open("/search/downLoad.do?page_cnt="+"3"+"&language="+"chi"+"&resourceType="+"type"+"&source="+"WF"+"&resourceId="+"kxyxxh201724025"+"&resourceTitle="+"简述利用Python网络爬虫实现多下载站软件搜索及下载地址提取"+"&isoa="+"0"+"&type="+"perio");
	/*}*/
}

// upload('3','kxyxxh201724025','chi','WF','简述利用Python网络爬虫实现多下载站软件搜索及下载地址提取','0','perio')