package com.example.p2pgeocaching.caches

import android.util.Log
import com.example.p2pgeocaching.RSA.RSA

/**
 * This class saves all the data related to a cache.
 * Cache class can be called in two ways, either to create a new cache or to save an existing one.
 * The title of the cache is saved in [title], its description in [desc], neither may contain an
 * illegal character.
 * [creator] contains the name of the cache's creator, also no illegal characters allowed.
 * The unique identifier [id] is generated by concatenating [title], ';', [desc], then hashing them.
 * The public key is saved in [pubKey], the private key  in [prvKey].
 * The [hallOfFame] contains the encrypted name of the people that have completed the cache.
 * It saves them as an array of Strings.
 * The only item contained at initialization is the [creator].
 * To decrypt, the [pubKey] is used.
 * For encrypting, you need the [prvKey], which you receive upon finding the physical cache.
 * [plainTextHOF] contains the plain text that [hallOfFame] encrypts.
 */
open class Cache(
    val title: String,
    val desc: String,
    val creator: String,
    var id: Int,
    var pubKey: String?,
    var prvKey: String?,
    var hallOfFame: MutableSet<String>,
    var plainTextHOF: String
) {

    companion object {
        const val TAG = "Cache"
    }


    /**
     * When a constructor is called without a [hallOfFame], it passes an empty set.
     */
    constructor(
        title: String,
        desc: String,
        creator: String,
        id: Int,
        pubKey: String?,
        prvKey: String?
    ) : this(title, desc, creator, id, pubKey, prvKey, mutableSetOf(), "")


    /**
     * This function takes an String containing a cipher text [cipherText] as input
     * It returns the plain text as a String.
     * This decryption is done using the public key.
     *
     */
    private fun decryptToString(cipherText: String): String {
        return RSA.decode(cipherText, pubKey)
    }


    /**
     * This function decrypts the [hallOfFame] and returns it as a String.
     * Each entry of [hallOfFame] is separated by a new line in the final String.
     * If [hallOfFame] is null, an empty string is returned.
     */
    fun hallToString(): String {
        var hofString = ""
        return run {
            for (cipherEntry in hallOfFame) {
                hofString += decryptToString(cipherEntry) + "\n"
            }
            Log.d(TAG, "The hall of fame string is: $hofString")
            hofString
        }
    }


    /**
     * A simple function which updates the [plainTextHOF] parameter with the current [hallOfFame].
     */
    protected fun updatePlainTextHOF() {
        plainTextHOF = hallToString()
    }


    /**
     * This function is used to add any number of people to the list
     */
    fun addPeopleToHOF(people: Set<String>) {
        // Add the people to HOF
        for (person in people) {
            hallOfFame.add(person)
        }
        updatePlainTextHOF()
    }


    /**
     * Simple function that calls the addPeopleToHOF() function, with its input cast to a set.
     */
    fun addPersonToHOF(person: String) {
        addPeopleToHOF(setOf(person))
    }


    /**
     * The toString() function now concatenates most things in human readable format.
     * Format is as follows: "<name>: <data>;", repeated.
     */
    override fun toString(): String {
        return "Title: $title; Description: $desc; Creator: $creator; ID: $id; " +
                "Public Key: ${pubKey.toString()}; Private key: ${prvKey.toString()}; " +
                "Hall of Fame: ${hallOfFame}; Text in Hall of Fame: $plainTextHOF"
    }
}