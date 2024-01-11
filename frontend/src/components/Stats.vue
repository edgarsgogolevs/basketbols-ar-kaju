<script setup>

const props = defineProps({
    game: { type: Object, default: null },
});

</script>

<template>
    <div class="stats-grid">
        <div class="team">
            <div class="team-card" v-tooltip="'The number of successful passes leading to scored points by teammates'">
                <div class="team-card-info">
                    <i class="mdi mdi-account-arrow-right big-icon" ></i>
                    <p class="game-points">{{ game.AST }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Assists
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The number of successful blocks on opponents shots'">
                <div class="team-card-info">
                    <i class="mdi mdi-block-helper big-icon" ></i>
                    <p class="game-points">{{ game.BLK }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Blocks
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The number of times the player grabbed the ball in defensive situations'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball big-icon" ></i>
                    <p class="game-points">{{ game.DREB }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Defensive Rebounds
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The total number of attempts to make three-point shots'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball-hoop-outline big-icon" ></i>
                    <p class="game-points">{{ game.FG3A }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Three-Point Field Goals Attempted
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The number of successful three-point shots'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball-hoop big-icon" ></i>
                    <p class="game-points">{{ game.FG3M }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Three-Point Field Goals Made
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The ratio of successful three-point shots to the total number of attempts'">
                <div class="team-card-info">
                    <i class="mdi mdi-percent-outline big-icon" ></i>
                    <p class="game-points">{{ (game.FG3_PCT*100).toFixed(0) }}%</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Three-Point Field Goal Percentage
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="' The total number of attempts to make field goals'">
                <div class="team-card-info">
                    <i class="mdi mdi-target big-icon" ></i>
                    <p class="game-points">{{ game.FGA }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Field Goals Attempted
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of successful field goals'">
                <div class="team-card-info">
                    <i class="mdi mdi-target-variant big-icon" ></i>
                    <p class="game-points">{{ game.FGM }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                             Field Goals Made
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The ratio of successful field goals to the total number of attempts'">
                <div class="team-card-info">
                    <i class="mdi mdi-percent big-icon" ></i>
                    <p class="game-points">{{ (game.FG_PCT*100).toFixed(0) }}%</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Field Goal Percentage 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The total number of attempts to make free throws'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball-hoop-outline big-icon" ></i>
                    <p class="game-points">{{ game.FTA }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Free Throws Attempted 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of successful free throws'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball-hoop big-icon" ></i>
                    <p class="game-points">{{ game.FTM }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Free Throws Made 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The ratio of successful free throws to the total number of attempts'">
                <div class="team-card-info">
                    <i class="mdi mdi-percent-outline big-icon" ></i>
                    <p class="game-points">{{ (game.FT_PCT*100).toFixed(0) }}%</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Free Throw Percentage  
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The total amount of time the player spent on the court'">
                <div class="team-card-info">
                    <i class="mdi mdi-clock-outline big-icon" ></i>
                    <p class="game-points">{{ game.MIN }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Minutes 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of times the player grabbed the ball in offensive situations'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball big-icon" ></i>
                    <p class="game-points">{{ game.OREB }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Offensive Rebounds 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of fouls committed by the player'">
                <div class="team-card-info">
                    <i class="mdi mdi-whistle-outline big-icon" ></i>
                    <p class="game-points">{{ game.PF }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Personal Fouls 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of successful steals of the ball'">
                <div class="team-card-info">
                    <i class="mdi mdi-basketball big-icon" ></i>
                    <p class="game-points">{{ game.REB }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Rebounds 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of times the player lost possession of the ball'">
                <div class="team-card-info">
                    <i class="mdi mdi-hand-heart big-icon" ></i>
                    <p class="game-points">{{ game.STL }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Steals 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="team">
            <div class="team-card" v-tooltip="'The number of times the player lost possession of the ball'">
                <div class="team-card-info">
                    <i class="mdi mdi-rotate-3d-variant big-icon" ></i>
                    <p class="game-points">{{ game.TOV }}</p>
                    <div class="span-row">
                        <p class="ba-description">
                            Turnovers 
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>