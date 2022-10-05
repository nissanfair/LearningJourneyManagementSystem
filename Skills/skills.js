const app1 = Vue.createApp({
    data() {
      return {
        // name:value pairs here
        // cannot use variables in another variable as you are declaring here
        message: "Choose your favorite fruit:", // generic
        skills : "",// Placeholder for now it is to hold all the skills coming from the back end
      }
    },
    methods: {

    },
    created() {
        url = "http://10.124.131.144:5000/skill";
        axios
          .get(url)
          .then((response) => {
            // process response.data object
            console.log(response.data.data.skills);
            this.skills = response.data.data.skills;
          })
          .catch((error) => {
            // process error object
          });
      },
      
  })
  // (2) Link (mount) Vue instance to DOM
  const vm = app1.mount('#app');