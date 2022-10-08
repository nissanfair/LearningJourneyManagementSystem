const app1 = Vue.createApp({
    data() {
      return {
        // name:value pairs here
        // cannot use variables in another variable as you are declaring here
        message: "Choose your favorite fruit:", // generic
        jobroles : "",// Placeholder for now it is to hold all the skills coming from the back end
      }
    },
    methods: {

    },
    created() {
        url = "http://10.124.131.144:5000/jobrole"; //number is wrong
        axios
          .get(url)
          .then((response) => {
            // process response.data object
            console.log(response.data.data.jobrole_name);
            this.jobroles = response.data.data.jobrole_name;
          })
          .catch((error) => {
            // process error object
          });
      },
      
  })
  // (2) Link (mount) Vue instance to DOM
  const vm = app1.mount('#app');