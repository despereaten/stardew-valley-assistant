<template>
  <div>
    <div id="loader-container" v-if="!response && validUrl" :style="{ width: cardWidth }">
      <slot name="loading">
        <div class="spinner"></div>
      </slot>
    </div>
    <div v-if="response">
      <slot :img="image" :title="response.title" :description="response.description" :url="url">
        <div class="wrapper" :style="{ width: cardWidth }">
          <div class="card-img">
            <img :src="image" />
          </div>
          <div class="card-info">
            <div class="card-text">
              <h1>{{ response.title }}</h1>
              <p>{{ response.description }}</p>
            </div>
            <div class="card-btn">
              <a href="javascript:;" v-if="showButton" @click="viewMore">View More</a>
            </div>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script>
import FIBSImage from "../assets/guesslike/F.I.B.S..png";
import Festival_of_Ice_2 from "../assets/guesslike/600px-Festival_of_Ice_2.png";
import NightMarket from "../assets/guesslike/600px-NightMarket.png";
import Fortune_Teller from "../assets/guesslike/Fortune_Teller.png";
import House from "../assets/guesslike/House.png";
import Livin_Off_The_Land from "../assets/guesslike/Livin'_Off_The_Land.png";
import Queen_of_Sauce from "../assets/guesslike/Queen_of_Sauce.png";
import Weather_Report_Fern_Islands from "../assets/guesslike/Weather_Report_Fern_Islands.png";
import Weather_Report from "../assets/guesslike/Weather_Report.png";
import Desert_Festival from "../assets/guesslike/600px-Desert_Festival.png";
import Flower_Festival from "../assets/guesslike/600px-Flower_Festival.png";
import Warp_Totem_Beach from "../assets/guesslike/600px-Warp_Totem_Beach_location.png";
import SecretWoods from "../assets/guesslike/SecretWoods.png";

export default {
  name: "link-prevue",
  props: {
    url: {
      type: String,
      default: "",
    },
    cardWidth: {
      type: String,
      default: "400px",
    },
    onButtonClick: {
      type: Function,
      default: undefined,
    },
    showButton: {
      type: Boolean,
      default: true,
    },
    apiUrl: {
      type: String,
      default: "https://link-preview-api.nivaldo.workers.dev/preview",
    },
  },
  watch: {
    url: function () {
      this.response = null;
      this.image = null;
      this.getLinkPreview();
    },
  },
  created() {
    this.getLinkPreview();
  },
  data: function () {
    return {
      response: null,
      image: null,
      validUrl: false,
      fallbackImages: [
        FIBSImage,
        Festival_of_Ice_2,
        NightMarket,
        Fortune_Teller,
        House,
        Livin_Off_The_Land,
        Queen_of_Sauce,
        Weather_Report_Fern_Islands,
        Weather_Report,
        Desert_Festival,
        Flower_Festival,
        Warp_Totem_Beach,
        SecretWoods,
      ],
    };
  },
  methods: {
    viewMore: function () {
      if (this.onButtonClick !== undefined) {
        this.onButtonClick(this.response);
      } else {
        const win = window.open(this.url, "_blank");
        win.focus();
      }
    },
    isValidUrl: function (url) {
      const regex = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/;
      this.validUrl = regex.test(url);
      return this.validUrl;
    },
    getLinkPreview: function () {
      if (this.isValidUrl(this.url)) {
        this.httpRequest(
          (response) => {
            this.response = response;
            this.image = response.image || this.getRandomFallbackImage();
          },
          () => {
            this.response = null;
            this.validUrl = false;
          }
        );
      }
    },
    getRandomFallbackImage: function () {
      const randomIndex = Math.floor(Math.random() * this.fallbackImages.length);
      const selectedImage = this.fallbackImages[randomIndex];
      this.fallbackImages.splice(randomIndex, 1); // Remove the selected image to avoid duplicates
      return selectedImage;
    },
    httpRequest: function (success, error) {
      fetch(`${this.apiUrl}?url=${this.url}`)
        .then(response => response.json())
        .then(linkPreviewData => success(linkPreviewData))
        .catch(() => error());
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Hind+Siliguri:400,600");

.wrapper {
  width: 100%;
  max-width: 400px;
  border-radius: 7px 7px 7px 7px;
  background-color: #fff;
  -webkit-box-shadow: 0px 14px 32px 0px rgba(0, 0, 0, 0.15);
  -moz-box-shadow: 0px 14px 32px 0px rgba(0, 0, 0, 0.15);
  box-shadow: 0px 14px 32px 0px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-img {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 15px;
}

.card-img img {
  width: 80%;
  max-width: 100%;
  border-radius: 7px 7px 0 0;
}

img {
  vertical-align: middle;
  border-style: none;
}

.card-info {
  border-radius: 0 0 7px 7px;
  background-color: #ffffff;
  
}

.card-text {
  width: 80%;
  margin: 0 auto;
  text-align: justify;
}

.card-text h1 {
  text-align: center;
  font-size: 20px;
  color: #a9460c;
  margin: 5px 0 5px 0;
  font-family: "Hind Siliguri", sans-serif;
}

.card-text p {
  font-family: "Hind Siliguri", sans-serif;
  color: #a9460c;
  font-size: 15px;
  overflow: hidden;
  margin: 0;
  text-align: center;
}

.card-btn {
  margin: 1em 0 1em 0;
  position: relative;
  text-align: center;
}

.card-btn a {
  border-radius: 1em;
  font-family: "Hind Siliguri", sans-serif;
  font-size: 12px;
  letter-spacing: 0.1em;
  color: #a9460c;
  background-color: #fcc587f0;
  padding: 8px 16px;
  text-align: center;
  display: inline-block;
  text-decoration: none !important;
  -webkit-transition: all 0.2s ease-in-out;
  -moz-transition: all 0.2s ease-in-out;
  -ms-transition: all 0.2s ease-in-out;
  -o-transition: all 0.2s ease-in-out;
  transition: all 0.2s ease-in-out;

  background-color: #fcc587f0;
  box-shadow: inset #8a390a 0 0 0 1px,
              inset #ba4d0d 0 0 0 2px,
              inset #ffa845 0 0 0 3px,
              inset #cd710f 0 0 0 4px,
              inset #ba4d0d 0 0 0 5px,
              inset #8a390a 0 0 0 6px;
}

.card-btn a:hover {
  background-color: #fdbd74f0;
}

/* Loader */
.spinner {
  margin-top: 40%;
  margin-left: 45%;
  height: 28px;
  width: 28px;
  animation: rotate 0.8s infinite linear;
  border: 5px solid #868686;
  border-right-color: transparent;
  border-radius: 50%;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
