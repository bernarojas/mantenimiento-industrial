<template lang="html">
    <div class="row">
        <div class="col">
            <div class="row contenerPrincipal pt-5 pb-5">
                <div class="container-fluid">
                    <div class="row">  
                        <div class="col mb-3">
                            <tr v-for="personajes in book">
                                
                                <h6>Nuevo ProyectoX</h6>
                                <td>{{personajes.fields.id}}</td>
                                <td>{{personajes.fields.title}}</td>
                                <td>{{personajes.fields.description}}</td>
                             
                            </tr>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data () {
        return {
            book: []
        }
    },
    mounted() {
        this.$http.get("/predecirFotos").then( (req) => this.book = rew.data)
    }
}
</script>

<style lang="css" scoped>
</style>