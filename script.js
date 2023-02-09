    var xhr = null;
    var arr = null;
    var statistics_data = null;

    getXmlHttpRequestObject = function () {
        if (!xhr) {
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    function getPorfolios() {
      xhr = getXmlHttpRequestObject();
      xhr.onreadystatechange = loadPortfolios;
      xhr.open("GET", "http://localhost:5000/porfolios", true);
      xhr.send(null);
    }

    function loadPortfolios() {
    if (xhr.readyState == 4 && xhr.status == 200) {
		arr = JSON.parse(xhr.responseText);

		for(let i=0;i<arr.length;i++){
			 var opt = document.createElement("option");
			 opt.value= arr[i].name;
			 opt.innerHTML = arr[i].name;

		    var select = document.getElementById("Porfolios");
            select.appendChild(opt);

			}
      loadStocks();
        }
    }

    function loadStocks(){
    var porfolioName= document.getElementById("Porfolios").value
    var index = arr.findIndex(obj => obj.name==porfolioName);
    var select = document.getElementById("stocks");
    select.size=6;
    select.innerHTML='';

  for(let i=0;i<arr[index].stonks.length;i++){
     var l = document.createElement("option");
     l.value= arr[index].stonks[i];
     l.innerHTML = arr[index].stonks[i];
     l.onclick = displayStockStatistics;
          select.appendChild(l);
    }
    getStatistics();

    }

    function getNews(){
      xhr = getXmlHttpRequestObject();
      xhr.onreadystatechange = loadNews;
      url = "http://localhost:5000/news"
      var select = document.getElementById("stocks");
      for (let i = 0; i < select.length; i++) {
          if (url.indexOf('?') === -1) {
              url = `${url}?array[]=${select.options[i].text}`
          } else {
              url = `${url}&array[]=${select.options[i].text}`
          }
      }
      xhr.open("GET", url, true);
      xhr.send(null);

    }

    function loadNews(){
     if (xhr.readyState == 4 && xhr.status == 200) {
       var news = JSON.parse(xhr.responseText);
       var destination = document.getElementById("news");

       for(let i = 0; i<news.data.length;i++){
         var newDiv = document.createElement("div");
         var headline = document.createElement("h3");
         headline.value=news.data[i].title;
         headline.innerHTML=news.data[i].title;
         newDiv.appendChild(headline);

         var image = document.createElement("img");
         image.src=news.data[i].image_url;
         newDiv.appendChild(image);

         var link = document.createElement("a");
         link.href = news.data[i].url;
         link.appendChild(newDiv);
         destination.appendChild(link)
       }
         getChartData()
       }
    }
    function display(element,data){
      if(data){
        element.innerHTML=data;
      }
      else{
        element.innerHTML="-"
      }
    }

    function getStatistics(){
      xhr = getXmlHttpRequestObject();
      xhr.onreadystatechange = loadStatistics;
      // asynchronous requests
      var select = document.getElementById("stocks");
      url = "http://localhost:5000/statistics";
      for (let i = 0; i < select.length; i++) {
          if (url.indexOf('?') === -1) {
              url = `${url}?array[]=${select.options[i].text}`
          } else {
              url = `${url}&array[]=${select.options[i].text}`
          }
      }
      xhr.open("GET", url, true);
      xhr.send(null);
    }

    function loadStatistics(){
      if (xhr.readyState == 4 && xhr.status == 200){
        statistics_data = JSON.parse(xhr.responseText);
        console.log(statistics_data);
        var portfolio_value = document.getElementById("portfolio_value");
      //  portfolio_value.value = statistics_data.portfolio_Data.total_cost;
        //portfolio_value.innerHTML = statistics_data.portfolio_Data.total_cost;
        display(portfolio_value,statistics_data.portfolio_Data.total_cost);

        var portfolio_return = document.getElementById("portfolio_return");
      //  portfolio_return.value = statistics_data.portfolio_Data.return;
      //  portfolio_return.innerHTML = statistics_data.portfolio_Data.return;
        display(portfolio_return,statistics_data.portfolio_Data.return);

        var portfolio_volume = document.getElementById("portfolio_volume");
      //  portfolio_return.value = statistics_data.portfolio_Data.return;
      //  portfolio_volume.innerHTML = statistics_data.portfolio_Data.voltality;
        display(portfolio_volume,statistics_data.portfolio_Data.voltality);
        getNews();
      }
    }
    function displayStockStatistics(){
      var select = document.getElementById("stocks");
      var value = select.value;
      var text = select.options[select.selectedIndex].text
      for(let i = 0; i<statistics_data.stock_data.length; i++){
        if(text === statistics_data.stock_data[i].symbol){
          var close = document.getElementById("close");
          //close.innerHTML=statistics_data.stock_data[i].close
          display(close,statistics_data.stock_data[i].close);

          var dividends = document.getElementById("dividends");
          //dividends.innerHTML=statistics_data.stock_data[i].dividends
          display(dividends,statistics_data.stock_data[i].dividends)

          var high = document.getElementById("high");
          //high.innerHTML=statistics_data.stock_data[i].high
          display(high,statistics_data.stock_data[i].high)

          var low = document.getElementById("low");
          //low.innerHTML=statistics_data.stock_data[i].low
          display(low,statistics_data.stock_data[i].low)

          var open = document.getElementById("open");
          //open.innerHTML=statistics_data.stock_data[i].open
          display(open,statistics_data.stock_data[i].open)

          var share_cost = document.getElementById("total_cost");
          //share_cost.innerHTML=statistics_data.stock_data[i].share_cost
          display(share_cost,statistics_data.stock_data[i].share_cost)

          var stock_wts = document.getElementById("weight_of_stock");
          //stock_wts.innerHTML=statistics_data.stock_data[i].stock_wts
          display(stock_wts,statistics_data.stock_data[i].stock_wts)

          var total_shares = document.getElementById("Num_of_Shares");
          //total_shares.innerHTML=statistics_data.stock_data[i].total_shares
          display(total_shares,statistics_data.stock_data[i].total_shares)

          var volume = document.getElementById("volume");
        //  volume.innerHTML=statistics_data.stock_data[i].volume
          display(volume,statistics_data.stock_data[i].volume)
        }
      }
    }

    function getChartData(){
      xhr = getXmlHttpRequestObject();
      xhr.onreadystatechange = loadChartData;
      url = "http://localhost:5000/chart"
      var select = document.getElementById("stocks");
      for (let i = 0; i < select.length; i++) {
          // Check to see if the URL has a query string already
          if (url.indexOf('?') === -1) {
              url = `${url}?array[]=${select.options[i].text}`
          } else {
              url = `${url}&array[]=${select.options[i].text}`
          }
      }
      xhr.open("GET", url, true);
      xhr.send(null);
    }

    function loadChartData(){
      if (xhr.readyState == 4 && xhr.status == 200){
        var chart_data = JSON.parse(xhr.responseText)
        console.log(chart_data);
        console.log(chart_data.portfolio_chart_data.dates);
        const data= {

                    //chart_data.portfolio_chart_data.dates,
                    //labels: ["jan","feb","mar","april","may","jun","jul","aug","sep","oct","nov","dec"],
                    labels: chart_data.portfolio_chart_data.dates,
                    datasets: [{
                      fill: false,
                      lineTension: 0,
                      borderColor: 'rgb(75, 192, 192)',
                      pointRadius: 0,
                      data: chart_data.portfolio_chart_data.data
                    }]
                  };
        var myChart = new Chart("myChart", {
          type: "line",
          data,
          options: {
            plugins:{
            legend: {
              display: false
            }
          },
            scales: {
              x: {
                grid: {
                    tickColor: "red"
                },
                ticks: {
                  callback: function(value, index, values)  {
                      if(index%30 === 0){
                        return data.labels[index].slice(5,17);
                      }
                    }
                  }
                }
            }
          }
    });
      }

    }
