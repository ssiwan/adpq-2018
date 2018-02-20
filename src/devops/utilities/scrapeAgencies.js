//
//		@author HOTB Software
//        This tool will scrape the list of agencies for the California State Department
//		  from the following url: http://www.ca.gov/agenciesall
//

/* Example Usage */
// scrapeAgencies((result) => {
// 	require('fs').writeFile('./my.json', JSON.stringify(result), (err) => { 
// 		if (err) { console.error('Crap happens') }
// 	})
// })

const https = require('http')
var cheerio = require('cheerio')

exports.scrapeAgencies = (completion) => {
	https.get('http://www.ca.gov/agenciesall', (response) => {
		var htmlStr = ''

		response.on('data', (chunk) => {
			htmlStr += chunk
		})

		response.on('end', () => {
			var $ = cheerio.load(htmlStr)
			
			var agencyArray = []
			$('#list').find('li').each(function(i, elm) {
				var str = $(this).text()
				var parsedStr = str.split(/[\|]/)
				agencyArray.push(parsedStr[2].trim())
			})

			completion(agencyArray)
		})
	}).on("error", (err) => {
		console.log("Error: " + err.message);
	})
}