/*var getPhoto = new Vue(
{
    el: '#get-photo',
    delimiters: ['[[', ']]'],
    data: 
    {
      planetList: []
    },
  
    created: function() 
    {
      this.fetchPlanetList();
      this.timer = setInterval(this.fetchPlanetList, 10000);
    },
    methods: 
    {
        fetchPlanetList: function() 
        {
            axios
            .get('planets/')
            .then(response => (this.planetList = response.data.planets))
    
            console.log("I got the planets!");
            this.seen=false
            this.unseen=true
        },
        cancelAutoUpdate: function() 
        { 
            clearInterval(this.timer) 
        }
    },
    beforeDestroy() 
    {
        clearInterval(this.timer)
    }
})
*/

var add_show_donations = new Vue
(
    {
        el: "#add-show-donations",
        delimiters: ['[[', ']]'],
        data:
        {
            donations: {},
            add_donations: [],
            donation_size: 0
        },

        created: function()
        {
            //this.fetchDonations();
        },
        methods:
        {
            makeRequest: function(event)
            {
                this.add_donations.push({item: "", amount: null})
                console.log("donation list size: " + this.donation_size);
            },
            submitDonations: function(payload) 
            {
                

                const config = {
                    headers: {
                      'Content-Type': 'application/x-www-form-urlencoded'
                    }
                };

                axios({
                    method: 'post',
                    url: '/fetch_donation/',
                    data: payload,
                    config: config
                  })
                  .then(response => (this.donations = response.data))
            },
            fetchDonations: function()
            {
                axios
                    .get('/fetch_donation')
                    .then(response => {this.donations = response.data.donations;
                        });

                console.log(this.donations);
            }
        }   
    }
)

