<script setup>
	import { ref, reactive, toRef, shallowRef, onBeforeMount, computed, watch, defineAsyncComponent } from 'vue'
	//Used to store state form store in reactive variables
	import { storeToRefs } from "pinia" 
	//Import authentication store
	import { useAuthStore } from "./stores/AuthStore"
	import { useRoute, useRouter } from "vue-router"
	//Import components
	import SideNavigation from "./components/SideNavigation.vue"
	import SuggestionCard from "./components/SuggestionCard.vue"
	import SearchBar from "./components/SearchBar.vue"
	//Register async components, they'll be donwloadod only when rendered
	const LoginModal = defineAsyncComponent(() => import("./components/modals/LoginModal.vue"))
	const RegisterModal = defineAsyncComponent(() => import("./components/modals/RegisterModal.vue"))
	const ForgotPasswordModal = defineAsyncComponent(() => import("./components/modals/ForgotPasswordModal.vue"))
	const ResetPasswordModal = defineAsyncComponent(() => import("./components/modals/ResetPasswordModal.vue"))
	const router = useRouter()
	const route = useRoute()

	const friendSuggestions = [
		{src: 'https://sogor98.eu.pythonanywhere.com/assets/img/default-profile-image.jpeg', name: 'Elon Musk', handle: '@teslaBoy'},
		{src: 'https://sogor98.eu.pythonanywhere.com/assets/img/default-profile-image.jpeg', name: 'Adrian Monk', handle: '@detective:)'},
		{src: 'https://sogor98.eu.pythonanywhere.com/assets/img/default-profile-image.jpeg', name: 'Kevin Hart', handle: '@miniRock'}
	];


	//Authentication logic
	//Define the store
	const authStore = useAuthStore()
	//Get auth state from store
	const { auth } = storeToRefs(authStore)

	const handleLogin = (form) => {
		authStore.login(form)
	}

	const handleRegistration = (form) => {
		console.log("registering")
		authStore.register(form)
	}

	const handleForgotPassword = (form) => {
		authStore.forgotPassword(form)
	}

	const handleResetPassword = (form) => {
		authStore.resetPassword(form, route.query.token)
	}

	const handleLogout = () => {
		console.log("logging out from app")
		authStore.logout()
		router.replace("/")
	}

	//Try login before app mounts, if token cookie present run login logic
	//Used for page refresh and revisits during the cookie lifetime (3 days)
	onBeforeMount(() => {
		handleLogin()
	})

	//Modal controls
	//Either LoginModal, RegisterModal or ForgotPasswordModal components(!)
	const modalToShow = shallowRef(null) //shallowRef for better performance, doesn't react to deep changes
	const isModalLoading = ref(false)
	//Watch route hash to trigger modal opening and closing
	watch(
		()=> route.hash,
		(newVal, oldVal) => {
			console.log(newVal, oldVal)
			handleOpenModal(newVal.replace("#", ""))
		}
	)


	const handleOpenModal = (type) => {
		switch(type){
			case "LoginModal":
				modalToShow.value = LoginModal
				break
			case "RegisterModal":
				modalToShow.value = RegisterModal
				break
			case "ForgotPasswordModal":
				modalToShow.value = ForgotPasswordModal
				break
			case "ResetPasswordModal":
				modalToShow.value = ResetPasswordModal
		}
	}

	const handleCloseModal = () => {
		router.push({hash: ""})
		modalToShow.value = null
		isModalLoading.value = false
	}

	const handleModalSubmit = (form) => {
		//set loading state
		isModalLoading.value = true
		//the paramter is the form itself that gets emitted from the modals
		switch(route.hash.replace("#", "")) {
			case "LoginModal":
				handleLogin(form)
				break
			case "RegisterModal":
				handleRegistration(form)
				break
			case "ForgotPasswordModal":
				handleForgotPassword(form)
			case "ResetPasswordModal":
				handleResetPassword(form)
		}
	}

	//Watch for auth state changes, if login succesful close modals
	watch(
		() => auth.value,
		(newVal) => {
			//If newVal is truthy (meaning the login is susccesful and auth state is populated)
			//close the modals
			newVal && handleCloseModal()
		}
	)


</script>

<template>
  <div class="flex w-full h-screen xl:container">
	  <SideNavigation 
	  	:user="auth" 
		  @open-login="router.push({hash: '#LoginModal'})"
		  @open-registration="router.push({hash: '#RegisterModal'})" 
		  @logout="handleLogout" 
		/>

    <!-- Main content area -->
    <main class="w-full h-full overflow-y-scroll md:w-1/2">
		<header class="sticky top-0 flex items-center justify-between w-full px-5 py-3 bg-white border-b border-lighter">
			<h1 class="text-xl font-bold">{{$route.name}}</h1>
			<SearchBar />
		</header>
		<router-view />
    </main>
	<!--End of Main content area-->

    <!-- trending -->
    <aside class="relative hidden w-1/3 h-full px-6 py-2 overflow-y-scroll border-l md:block border-lighter">
     

	<section class="w-full my-4 rounded-lg bg-lightest">
		<p class="p-3 text-lg font-bold">Who to Follow</p>
		<SuggestionCard v-for="suggestion in friendSuggestions" :key="suggestion.handle" :friendSuggestion="suggestion" />
	</section>

    </aside>
	<component :is="modalToShow" :isLoading="isModalLoading" v-if="modalToShow && !auth" @submit-form="handleModalSubmit" @close="handleCloseModal"/>
	<notifications position="bottom left"/>
  </div>
</template>
